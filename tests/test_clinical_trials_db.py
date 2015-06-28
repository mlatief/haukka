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
        m = hashlib.md5()
        m.update(self.clinical_trial1)
        checksum = m.hexdigest()
        ct_id = self.db.insert_clinical_trial_xml(self.nct_id1, self.clinical_trial1, checksum)
        self.assertEqual(ct_id, self.nct_id1)

    def test_get_clinical(self):
        pass


if __name__ == '__main__':
    unittest.main()
