from flask_restful import Resource, reqparse
from pyhaukka.app import get_db

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)
parser.add_argument('limit', type=int, default=20)
parser.add_argument('offset', type=int, default=0)

class Trials(Resource):
    def get(self):
        # Query parameters: query=None, offset=0, limit=20
        db = get_db()
        args = parser.parse_args()
        q = args['query']
        l = args['limit']
        o = args['offset']

        if q :
            r = db.search_clinical_trials(q, l, o)
        else:
            r = db.get_all_clinical_trials(l, o)

        return {'trials':r}
