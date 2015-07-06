import unittest
import os
import pyhaukka.db

db = pyhaukka.db.ClinicalTrialsDatabase(os.environ.get('DATABASE_URL'))


class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        self.db = db.connect()
        self.assertIsNotNone(self.db)
        self.db.close()

if __name__ == '__main__':
    unittest.main()