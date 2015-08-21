__author__ = 'mlatief'

import unittest
import nltk
from nltk.tokenize import wordpunct_tokenize
from pyhaukka.classify import BiomarkerClassifier, store_pickled, load_pickled

class ClassifierTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        train = "Diagnosis of locally advanced or metastatic melanoma along " \
                "with written documentation of [BRAF V600] mutation."
        train_tree = nltk.chunk.tagstr2tree(train, chunk_label="BIO")
        cls.classifier = BiomarkerClassifier(train_tree)

    def test_tag_performance(self):
        import requests
        from bs4 import BeautifulSoup
        r = requests.get('https://clinicaltrials.gov/show/NCT02034110?displayxml=true')
        raw = BeautifulSoup(r.text, "html.parser").get_text()
        tags = self.classifier.tag(raw)
        assert tags is not None