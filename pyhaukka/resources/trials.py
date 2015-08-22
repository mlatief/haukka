from flask_restful import Resource, reqparse
from flask import abort
import ujson

class Trials(Resource):
    def get(self):
        from pyhaukka.app import app, db
        from pyhaukka.models import Trial

        # Query parameters: q=None, offset=0, limit=20
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, help='Biomarkers query')
        args = parser.parse_args()
        q = args['q']
        print "Request with query: ", q
        all_trials = db.session.query(Trial).all()
        trials=[ct.get_json() for ct in all_trials]
        return trials

class TrialResource(Resource):
    def get(self, trial_id):
        from pyhaukka.app import db
        from pyhaukka.models import Trial

        q = db.session.query(Trial)
        r = q.get(trial_id)
        if not r:
            abort(404)
        return r.get_json()
