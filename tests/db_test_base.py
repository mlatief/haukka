import os
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', "postgresql://haukka:@localhost/haukka_test?connect_timeout=5")

import xml.etree.ElementTree as ET
import unittest
import hashlib
import pyhaukka.db

db = pyhaukka.db.ClinicalTrialsDatabase(os.environ['DATABASE_URL'])


class HaukkaDbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = db.connect()
        # Explicitly start a transaction so changes can be rolled-back at connection close
        self.db.begin()
        # Reinitialize clean tables!
        self.db.execute(open("tests/schema.sql", "r").read())

    def tearDown(self):
        self.db.rollback()
        self.db.close()
        del self.db
        self.db = None

    @classmethod
    def setUpClass(cls):
        # Load test trials fixtures from xml files
        nct_ids = ['NCT02034110', 'NCT00001160', 'NCT00001163']
        cls.trials = []
        for nctid in nct_ids:
            with open("data/{}.xml".format(nctid)) as ct:
                ct_xml = ct.read()

                m = hashlib.md5()
                m.update(ct_xml)
                ct_checksum = m.hexdigest()

                root = ET.fromstring(ct_xml)
                ct_status = root.findtext('./overall_status')
                trial = {'id': nctid, 'xml': ct_xml, 'status': ct_status, 'checksum': ct_checksum}
                cls.trials.append(trial)

        if len(cls.trials) < len(nct_ids):
            raise Exception("Couldn't read all test data...")
