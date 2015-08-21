import unittest
from manage import train
import os

class MyTestCase(unittest.TestCase):
    def test_something(self):
        train()
        assert os.path.isfile('nltk_data/classifier/biomarker_classifier.pickle')

if __name__ == '__main__':
    unittest.main()
