import logging
log = logging.getLogger(__name__)

import unittest
from config import TEST_DATABASE_URI
from pyhaukka.models import Trial

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

from fixture import load_sample_trials

class TrialModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global transaction, connection, engine

        # Connect to the database and create the schema within a transaction
        engine = create_engine(TEST_DATABASE_URI)
        connection = engine.connect()
        transaction = connection.begin()
        Trial.metadata.create_all(connection)

        # Load test trials fixtures from xml files
        nct_ids = ['NCT02034110', 'NCT00001160', 'NCT00001163']
        cls.trials = load_sample_trials(nct_ids)

    @classmethod
    def tearDownClass(cls):
        # Roll back the top level transaction and disconnect from the database
        transaction.rollback()
        connection.close()
        engine.dispose()

    def setUp(self):
        self.__transaction = connection.begin_nested()
        self.session = Session(connection)

    def tearDown(self):
        self.session.close()
        self.__transaction.rollback()

    def test_add(self):
        trial = Trial(ct_dict=self.trials[0])
        self.session.add(trial)


if __name__ == '__main__':
    unittest.main()
