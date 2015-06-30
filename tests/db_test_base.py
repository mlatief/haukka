import xml.etree.ElementTree as ET
import unittest
import hashlib
import pyhaukka.db

import psycopg2

# User Passwords are loaded from %APPDATA%\postgresql\pgpass.conf by the driver
PRE_POSTGRES_URL = "user='postgres'" # Connect with postgres user to create a DB

TEST_DB = 'haukka_test'
TEST_DB_USER = 'haukka'
POSTGRES_URL = "dbname='{}' user='{}'".format(TEST_DB, TEST_DB_USER)


class HaukkaDbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = pyhaukka.db.ClinicalTrialsDatabase(POSTGRES_URL)
        self.db.execute("BEGIN;")

    def tearDown(self):
        self.db.execute("ROLLBACK;")
        del self.db
        self.db = None

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
                trial = {'id': id, 'xml': ct_xml, 'status': ct_status, 'checksum': ct_checksum}
                cls.trials.append(trial)

        if len(cls.trials) < len(nct_ids):
            raise Exception("Couldn't read all test data...")

        with psycopg2.connect(PRE_POSTGRES_URL) as conn:
            conn.autocommit=True
            cls.db_created = False
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DB,))
                r = cur.fetchone()
                if r is None:
                    cur.execute('CREATE DATABASE {};'.format(TEST_DB))
                    cls.db_created = True

        with psycopg2.connect(POSTGRES_URL) as conn:
            conn.autocommit=True
            with conn.cursor() as cur:
                cur.execute(open("schema.sql", "r").read())

    @classmethod
    def tearDownClass(cls):
        if cls.db_created:
            with psycopg2.connect(PRE_POSTGRES_URL) as conn:
                conn.autocommit=True
                with conn.cursor() as cur:
                    cur.execute('DROP DATABASE {};'.format(TEST_DB))
                    print "... dropped db!"
                    cls.db_created = False

