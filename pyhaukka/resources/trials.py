from flask_restful import Resource
from pyhaukka.app import get_db

class Trials(Resource):
    def get(self):
        # Query parameters: query=None, page=0, count=20
        db = get_db()

        r = db.get_all_clinical_trials()
        return {'trials':r}
