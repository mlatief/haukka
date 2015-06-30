from db_test_base import HaukkaDbTestCase
import unittest
import hashlib

class ClinicalTrialsTestCase(HaukkaDbTestCase):
    def test_execute(self):
        '''
        Doesn't make sense to test this specific method,
        as it should be working already in order for setUp to work properly (as well as tearDown later)
        '''
        pass

    def test_insert_clinical_trial_xml(self):
        ct = self.trials[0]
        ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
        self.assertEqual(ct_id, ct['id'])

    def test_get_clinical(self):
        ct = self.trials[0]
        ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
        self.assertEqual(ct_id, ct['id'])

        r = self.db.get_clinical_trial_by_id(ct['id'])
        self.assertEqual(r['nctid'], ct_id)
        self.assertEqual(r['checksum'], ct['checksum'])
        self.assertIsNotNone(r['ctdata'])
        self.assertIsNotNone(r['inserted'])

        ctdata = r['ctdata']
        self.assertIsNotNone(ctdata['clinical_study'])
        self.assertIsNotNone(ctdata['clinical_study']['id_info'])
        self.assertIsNotNone(ctdata['clinical_study']['id_info']['nct_id'])
        self.assertEqual(ctdata['clinical_study']['id_info']['nct_id'], ct_id)

        self.assertIsNotNone(ctdata['clinical_study']['overall_status'])
        self.assertEqual(ctdata['clinical_study']['overall_status'], ct['status'])
        # print 'United States' in ctdata['clinical_study']['location_countries']['country']

if __name__ == '__main__':
    unittest.main()
