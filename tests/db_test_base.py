import xml.etree.ElementTree as ET
import unittest
import hashlib
import pyhaukka.db

POSTGRESQL_URL = "dbname='{}' user='{}'".format('haukka_test', 'haukka')

class HaukkaDbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = pyhaukka.db.ClinicalTrialsDatabase(POSTGRESQL_URL)
        self.db.execute("BEGIN;")
        self.db.execute(open("schema.sql", "r").read())

    def tearDown(self):
        self.db.execute("ROLLBACK;")

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
        # Read test trials fixtures from xml files
        nct_ids = ['NCT00001160', 'NCT00001163',  'NCT02034110']
        cls.trials = []
        for id in nct_ids:
            with open("../data/{}.XML".format(id)) as ct:
                ct_xml = ct.read()

                m = hashlib.md5()
                m.update(ct_xml)
                ct_checksum = m.hexdigest()

                root = ET.fromstring(ct_xml)
                ct_status = root.findtext('./overall_status')
                print ct_status
                trial = {'id': id, 'xml': ct_xml, 'status': ct_status, 'checksum': ct_checksum}
                cls.trials.append(trial)


        if len(cls.trials) < len(nct_ids):
            raise Exception("Couldn't read all test data...")
