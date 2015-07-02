from pyhaukka.app import app
from db_test_base import HaukkaDbTestCase

from contextlib import contextmanager
from flask import appcontext_pushed, g

@contextmanager
def ct_db_set(db):
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
        if self.db.is_connected:
            self.db.close()

        del self.db
        self.db = None


    def check_content_type(self, headers):
      self.assertEqual(headers['Content-Type'], 'application/json')

