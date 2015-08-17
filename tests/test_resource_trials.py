from resource_test_base import ResourcesTestCase, app, db
from pyhaukka.models import Trial
import unittest
import ujson

class TrialsTestCase(ResourcesTestCase):

    def test_empty_db(self):
        with app.test_client() as c:
            rv = c.get('/trials')
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 0)

    def test_get_all_trials(self):
        for ct in self.trials:
            new_trial=Trial(ct_dict=ct)
            db.session.add(new_trial)

        with app.test_client() as c:
            rv = c.get('/trials')
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 3)

    def test_query_trials(self):
        ct_ids = []
        for ct in self.trials:
            new_trial=Trial(ct_dict=ct)
            db.session.add(new_trial)
            ct_ids.append(ct.get('nct_id'))

        with app.test_client() as c:
            rv = c.get('/trials?q=Cancer')
            self.check_content_type(rv.headers)

            data = ujson.loads(rv.data)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 3)

            ct = data[0]
            self.assertTrue(ct['nct_id'] in ct_ids)
            self.assertTrue('0203411' in ct['nct_id']) # Ordered by NCTID descending
            self.assertIsNotNone(ct['trial'])
            self.assertIsNotNone(ct['trial']['title'])
            self.assertIsNotNone(ct['trial']['overall_status'])

if __name__ == '__main__':
    unittest.main()
