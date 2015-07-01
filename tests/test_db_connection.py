from db_test_base import HaukkaDbTestCase

class ConnectionTestCase(HaukkaDbTestCase):
    def test_connection(self):
        self.assertIsNotNone(self.db)
