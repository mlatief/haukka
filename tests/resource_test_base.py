from pyhaukka.utils import init_loggers
init_loggers(log_file='tests.log')

from flask.ext.sqlalchemy import SQLAlchemy
import unittest
from pyhaukka.app import app, db
from config import TEST_DATABASE_URI

from pyhaukka.models import Trial

class ResourcesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fixture import load_sample_trials
        # Load test trials fixtures from xml files
        nct_ids = ['NCT02034110', 'NCT00001160', 'NCT00001163']
        cls.trials = load_sample_trials(nct_ids)

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        app.testing = True
        app.debug = True
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.session.close()

    def check_content_type(self, headers):
      self.assertEqual(headers['Content-Type'], 'application/json')

