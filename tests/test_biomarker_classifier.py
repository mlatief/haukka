import unittest
import nltk
from nltk.tokenize import wordpunct_tokenize
from pyhaukka.classify import BiomarkerClassifier, store_pickled, load_pickled

class ClassifierTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        train = u"Diagnosis of locally advanced or metastatic melanoma along " \
                u"with written documentation of [BRAF V600] mutation."
        train_tree = nltk.chunk.tagstr2tree(train, chunk_label="BIO")
        cls.classifier = BiomarkerClassifier(train_tree)

    def test_train(self):
        assert self.classifier.classifier is not None

    def test_tag(self):
        test = u"Subjects will need to have " \
               u"a fresh or frozen tumor tissue sample provided to confirm the BRAF V600E mutation status."
        tags = self.classifier.tag(test)
        assert tags[16] == ('BRAF', 'BIO')
        assert tags[17] == ('V600E', 'BIO')

    def test_tag_MET(self):
        test = u"Crizotinib in Pretreated Metastatic Non-small-cell Lung Cancer With MET Amplification"
        tags = self.classifier.tag(test)
        assert tags[10] == ('MET', 'BIO')

    def test_tag_met_en(self):
        test = u"within the same liver segment as long as the dose constraints to normal tissue can be met"
        tags = self.classifier.tag(test)

        assert tags[-1] == ('met', 'O')

    def test_store_pickled(self):
        import os
        store_pickled(self.classifier, root="nltk_data/classifiers/", fname="test_biomarker_classifier.pickle")
        assert os.path.isfile("nltk_data/classifiers/test_biomarker_classifier.pickle")

    def test_load_pickled(self):
        import os
        test_cl = load_pickled(root="nltk_data/classifiers/", fname="test_biomarker_classifier.pickle")
        assert test_cl is not None

        test = u"Subjects will need to have " \
               u"a fresh or frozen tumor tissue sample provided to confirm the BRAF V600E mutation status."
        tags = test_cl.tag(test)
        assert tags[16] == ('BRAF', 'BIO')
        assert tags[17] == ('V600E', 'BIO')
