from pyhaukka.app import app
from db_test_base import HaukkaDbTestCase

from pyhaukka.utils import init_logger

log = init_logger('resource_test_base')


class PyhaukkaTestCase(HaukkaDbTestCase):
    def setUp(self):
        super(PyhaukkaTestCase, self).setUp()
        app.db = self.db
        self.app = app

    def tearDown(self):
        # Rollback should have been performed since AppContext should close the connection without a commit!
        if self.db.is_connected():
            log.warn('Connection is still open, connection will be closed explicitly!')
            self.db.close()

    def check_content_type(self, headers):
      self.assertEqual(headers['Content-Type'], 'application/json')

