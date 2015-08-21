import unittest
from manage import train
import os

class TrainingTestCase(unittest.TestCase):
    def test_trainer(self):
        train()
        assert os.path.isfile('nltk_data/classifiers/biomarker_classifier.pickle')

if __name__ == '__main__':
    unittest.main()
