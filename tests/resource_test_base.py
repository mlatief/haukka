from pyhaukka.app import app
from db_test_base import HaukkaDbTestCase, TEST_DB_URL
import unittest

from contextlib import contextmanager
from flask import appcontext_pushed, g

@contextmanager
def ct_db_set(app, db):
    def handler(sender, **kwargs):
        g._database = db
    with appcontext_pushed.connected_to(handler, app):
        yield

class PyhaukkaTestCase(HaukkaDbTestCase):
    def setUp(self):
        super(PyhaukkaTestCase, self).setUp()
        app.config['TESTING'] = True
        self.app = app

    def tearDown(self):
        # Rollback is performed automatically since AppContext close the connection without a commit
        pass

    def check_content_type(self, headers):
      self.assertEqual(headers['Content-Type'], 'application/json')

