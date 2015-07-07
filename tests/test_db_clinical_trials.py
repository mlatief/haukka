from db_test_base import HaukkaDbTestCase
import unittest


# TODO: Add paging test cases for get_all and search_clinical_trials

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

    def test_get_clinical_trial_by_id(self):
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

    def test_get_all_clinical_trials(self):
        ct_ids = []
        for ct in self.trials:
            ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
            ct_ids.append(ct_id)

        r = self.db.get_all_clinical_trials()
        self.assertIsNotNone(r)
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 3)

        ct = r[0]
        self.assertIsNotNone(ct)
        self.assertEqual(ct['nctid'], max(ct_ids)) # Ordered by NCTID, first is the highest
        self.assertIsNotNone(ct['ctdata'])
        self.assertIsNotNone(ct['ctdata']['clinical_study'])

    def test_search_clinical_trials_basic(self):
        q = "Eastern BRAF"

        ct_ids = []
        for ct in self.trials:
            ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
            ct_ids.append(ct_id)

        r = self.db.search_clinical_trials(q)
        self.assertIsNotNone(r)
        self.assertIsInstance(r, list)
        self.assertTrue(len(r) >= 1)

        ct = r[0]
        self.assertIsNotNone(ct)
        self.assertTrue(ct['nctid'] in ct_ids)
        self.assertIsNotNone(ct['headline'])
        self.assertIsNotNone(ct['ctdata'])
        self.assertIsNotNone(ct['rank'])

    @unittest.skip('Biomarkers aliases not yet supported')
    def test_search_clinical_trials_expansion(self):
        q = "BRAF-1" # BRAF, ..

        ct_ids = []
        for ct in self.trials:
            ct_id = self.db.insert_clinical_trial_xml(ct['id'], ct['xml'], ct['checksum'])
            ct_ids.append(ct_id)

        r = self.db.search_clinical_trials(q)
        self.assertIsNotNone(r)
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 1)

        ct = r[0]
        self.assertIsNotNone(ct)
        self.assertTrue(ct['nctid'] in ct_ids)

if __name__ == '__main__':
    unittest.main()
