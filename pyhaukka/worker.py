from celery import Celery

celery_app = Celery(__name__)
celery_app.config_from_object('celeryconfig')

import pyhaukka.classify
classifier = pyhaukka.classify.load_pickled()

@celery_app.task(bind=True)
def process_trial(self, url):
    import requests
    from pyhaukka.utils import convert_trial_xml_to_json
    from bs4 import BeautifulSoup

    from pyhaukka.app import app, db
    from pyhaukka.models import Trial
    import urllib2

    self.update_state(state='PROGRESS', meta={'status': "Fetching URL" })
    r = requests.get(url, headers={'Accept': "application/xml"})
    if r.status_code != 200:
        raise urllib2.HTTPError(url, r.status_code, r.reason, r.headers, None)

    if r:
        self.update_state(state='PROGRESS', meta={'status': "Parsing trial XML" })
        trial_dict = convert_trial_xml_to_json(r.text)
        nct_id = trial_dict.get('nct_id')
        lastchanged_date = trial_dict.get('lastchanged_date')

        old_trial = db.session.query(Trial).get(nct_id)
        if old_trial:
            if old_trial.lastchanged_date == lastchanged_date:
                raise ValueError("Duplicate trial with the same data found")

        self.update_state(state='PROGRESS', meta={'status': "Extracting RAW text" })
        raw = BeautifulSoup(r.text, "html.parser").get_text()

        self.update_state(state='PROGRESS', meta={'status': "Tagging Biomarkers" })
        tags = classifier.tag(raw)

        self.update_state(state='PROGRESS', meta={'status': "Collecting Biomarkers" })
        gner = [(t,v) for (t,v) in tags if v == 'BIO']

        self.update_state(state='PROGRESS', meta={'status': "Storing clinical trial" })
        if old_trial:
            old_trial.set_ct_fields(ct_dict=trial_dict, ners=gner)

        else:
            trial = Trial(ct_dict=trial_dict, ners=gner)
            db.session.add(trial)

        db.session.commit()
        return {'status': 'Trial processed!', 'result': nct_id}

    raise urllib2.URLError(reason="URL returned no response")



@celery_app.task
def bio_chunk_features(word):
    from pyhaukka.classify import en_words, cbio_words
    import re
    _digits = re.compile('\d')
    word_lower = word.lower()

    cbio = word in cbio_words
    all_caps = word.isupper()
    en_word = word_lower in en_words
    #stop_word = word_lower in stopwords.words()
    has_digits = bool(_digits.search(word_lower))

    # TODO: Add features such as:
    # - Followed by words such as mutations, wild-type, alteration
    # - Distance from such words
    # - Frequency distribution

    return {"cbio": cbio,
            "word": en_word,
            #"stop_word": stop_word,
            "all_caps": all_caps,
            "has_digits": has_digits}
