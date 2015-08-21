import logging, os
from logging.handlers import RotatingFileHandler

def init_loggers(log_file='app.log', level=logging.DEBUG):
    logger = logging.getLogger()

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))

    logger.addHandler(console)

    if os.environ.get('HEROKU') is None:
        console.setLevel(logging.INFO)
        rotating_file = logging.handlers.RotatingFileHandler(filename=log_file)
        rotating_file.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M'))
        logger.addHandler(rotating_file)

    logger.setLevel(level)

def print_elapsed(start):
    import time
    cur = time.clock()
    print("   {:03.2f} secs elapsed".format(cur-start))
    return cur


def dicts_subset_filter(d, subset, ignore_keys=[]):
    '''
    Checks if b is subset of a
    '''
    ka = set(d).difference(ignore_keys)
    kb = set(subset).difference(ignore_keys)
    return kb.issubset(ka) and all(d[k] == subset[k] for k in kb)

def convert_trial_xml_to_json(xml):
    from pyhaukka.converter import convert_xml_to_dict
    mapping = {'nct_id': './id_info/nct_id',
               'title': './official_title',
               'brief_summary': './brief_summary/textblock',
               'detailed_description': './detailed_description/textblock',
               'condition': ['./condition'],
               'overall_status': './overall_status',
               'location': ['./location_countries/country'],
               'keywords': ['./keyword'],
               'lastchanged_date': './lastchanged_date',
               'criteria': './eligibility/criteria/textblock'}
    d = convert_xml_to_dict(mapping, xml)
    return d

