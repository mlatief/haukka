import unittest
import my_testing_postgresql
import psycopg2
import pyhaukka.db
from datetime import datetime

# Temporary Database
postgresql = my_testing_postgresql.MyPostgresql(initdb='C:\\PostgreSQL\\9.4\\bin\\initdb.exe',
                                                postgres='C:\\PostgreSQL\\9.4\\bin\\postgres.exe')
print 'Initialized PostgreSQL instance!'

class HaukkaDbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = pyhaukka.db.ClinicalTrialsDatabase(postgresql.url())
        self.db.execute("BEGIN;")

    def tearDown(self):
        self.db.execute("ROLLBACK;")

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
        # Read test trials fixtures from xml files
        cls.nct_id1 = 'NCT00001160'
        cls.nct_id2 = 'NCT00001163'
        cls.nct_id3 = 'NCT02034110'

        with open('../data/NCT00001160.XML') as ct:
            cls.clinical_trial1 = ct.read()
        with open('../data/NCT00001163.XML') as ct:
            cls.clinical_trial2 = ct.read()
        with open('../data/NCT02034110.XML') as ct:
            cls.clinical_trial3 = ct.read()

        if cls.clinical_trial1 is None or cls.clinical_trial2 is None or cls.clinical_trial3 is None:
            raise Exception("Couldn't read all test data...")

        with psycopg2.connect(postgresql.url()) as conn:
            with conn.cursor() as cur:
                cur.execute(open("schema.sql", "r").read())

    @classmethod
    def tearDownClass(cls):
        pass
