import logging
log = logging.getLogger(__name__)

from pyhaukka.app import app
from db_test_base import HaukkaDbTestCase

class PyhaukkaTestCase(HaukkaDbTestCase):
    def setUp(self):
        super(PyhaukkaTestCase, self).setUp()
        app.db = self.db
        self.app = app

    def tearDown(self):
        # Rollback should have been performed since AppContext should close the connection without a commit!
        if self.db.is_connected():
            log.warn('Connection is still open, attempting to close connection...')
            self.db.close()

    def check_content_type(self, headers):
      self.assertEqual(headers['Content-Type'], 'application/json')

