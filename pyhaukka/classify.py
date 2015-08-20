import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import words, stopwords
import re

from nltk.tokenize import wordpunct_tokenize

corpus_root = "nltk_data/corpora/"
classifier_root = "nltk_data/classifiers"

cbio_corpus = PlaintextCorpusReader(corpus_root + '/cbio_cancer_genes', fileids=".+\\.txt")
_digits = re.compile('\d')


def bio_chunk_features(word):
    word_lower = word.lower()

    cbio = word in cbio_corpus.words()
    all_caps = word.isupper()
    en_word = word_lower in words.words()
    #stop_word = word_lower in stopwords.words()
    has_digits = bool(_digits.search(word_lower))

    # TODO: Add features such as:
    # - Followed by words such as mutations, wild-type, alteration
    # - Distance from such words
    # - Frequency distribution

    return {"cbio": cbio,
            "word": en_word,
            #"stop_word": stop_word,
            "all_caps": all_caps,
            "has_digits": has_digits}

class BiomarkerClassifier(nltk.TaggerI):
    def __init__(self, chunked_trial):
        # self.freq_dist = nltk.FreqDist(chunked_trial.words())
        # freq_dist = sorted(f.items(), key=lambda item: item[1])[:20]
        # {k:v for (k,v) in f.items() if v <= 10}  # choose only words with freq <= 10 least frequent

        train_set = list(self.get_features_from_chunk(chunked_trial))

        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def get_features_from_chunk(self, chunks_tree):
        if chunks_tree.height()>3:
            raise Exception("Chunk tree is too deep to parse!")

        for chunk in chunks_tree:
            if isinstance(chunk, nltk.Tree):
                for b in chunk:
                    yield (bio_chunk_features(b[0]), 'BIO')
            else:
                yield (bio_chunk_features(chunk[0]), 'O')

    def tag(self, sentence):
        sent_tokenized = wordpunct_tokenize(sentence)
        feats = [bio_chunk_features(word) for word in sent_tokenized]
        tags = self.classifier.classify_many(feats)
        conll = zip(sent_tokenized, tags)
        return conll

def store_pickled(classifier, root="nltk_data/classifiers", fname="biomarker_classifier.pickle"):
    import pickle
    import os
    fpath = os.path.join(root, fname)
    with open(fpath, "wb") as f:
        pickle.dump(classifier, f)

def load_pickled(root="nltk_data/classifiers", fname="biomarker_classifier.pickle"):
    import pickle
    import os
    fpath = os.path.join(root, fname)
    c = pickle.load(file(fpath))
    return c