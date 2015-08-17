from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON, ARRAY

class Trial(db.Model):
    __tablename__ = 'trials'

    nctid = db.Column(db.String, primary_key=True)
    url = db.Column(db.String())

    trial_data = db.Column(JSON)
    overall_status = db.Column(db.String())
    ner_result = db.Column(JSON)

    lastchanged_date = db.Column(db.DateTime)
    loaded_on = db.Column(db.DateTime)
    processed_on = db.Column(db.DateTime)

    def __init__(self, ct_dict, ners=None):
        self.set_ct_fields(ct_dict, ners)

    def set_ct_fields(self, ct_dict, ners=None):
        self.nctid=ct_dict.get('nct_id')
        self.url=ct_dict.get('url')
        self.lastchanged_date=ct_dict.get('lastchanged_date')
        self.overall_status=ct_dict.get('overall_status')
        self.loaded_on=datetime.now()
        self.trial_data=ct_dict
        if ners:
            self.ner_result=ners

    def get_json(self):
        return {
            'nct_id': self.nctid,
            'trial': self.trial_data,
            'ner_result': self.ner_result,
            'processed_on': self.processed_on
        }