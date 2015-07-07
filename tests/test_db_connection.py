from config import DATABASE_URI
import unittest
import pyhaukka.db

db = pyhaukka.db.ClinicalTrialsDatabase(DATABASE_URI)


class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        self.db = db.connect()
        self.assertIsNotNone(self.db)
        self.db.close()

if __name__ == '__main__':
    unittest.main()