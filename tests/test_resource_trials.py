from resource_test_base import PyhaukkaTestCase
import ujson
import unittest

class TrialsTestCase(PyhaukkaTestCase):
    def test_empty_db(self):
        with self.app.test_client() as c:
            rv = c.get('/trials')
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            self.assertIsNotNone(data)
            self.assertIsInstance(data.get('trials'), list)
            self.assertEqual(len(data['trials']), 0)

    def test_get_all_trials(self):
        ct_ids = []
        for ct in self.trials:
            ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
            ct_ids.append(ct_id)

        with self.app.test_client() as c:
            rv = c.get('/trials')
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            self.assertIsNotNone(data)
            self.assertIsInstance(data.get('trials'), list)
            self.assertEqual(len(data['trials']), 3)

    def test_query_trials(self):
        ct_ids = []
        for ct in self.trials:
            ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
            ct_ids.append(ct_id)

        with self.app.test_client() as c:
            rv = c.get('/trials?q=Cancer')
            self.check_content_type(rv.headers)

            data = ujson.loads(rv.data)
            self.assertIsNotNone(data)
            self.assertIsInstance(data.get('trials'), list)
            self.assertEqual(len(data['trials']), 3)

            ct = data['trials'][0]
            self.assertTrue(ct['nctid'] in ct_ids)
            self.assertTrue('0203411' in ct['nctid']) # Ordered by NCTID descending
            self.assertIsNotNone(ct.get('headline'))
            self.assertIsNotNone(ct['ctdata'])
            self.assertIsNotNone(ct['rank'])

if __name__ == '__main__':
    unittest.main()
