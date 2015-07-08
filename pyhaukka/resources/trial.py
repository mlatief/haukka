from flask_restful import Resource
from pyhaukka.app import get_db

class Trial(Resource):
    def get(self, trial_id):
        # Query parameters: q=None, offset=0, limit=20
        db = get_db()
        r = db.get_clinical_trial_by_id(trial_id)
        c = {'nctid': r['nctid'], 'ctdata': r['ctdata']}
        return c

    def put(self):
        pass