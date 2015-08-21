import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import words, stopwords

from nltk.tokenize import wordpunct_tokenize

corpus_root = "nltk_data/corpora/"
classifier_root = "nltk_data/classifiers"

cbio_corpus = PlaintextCorpusReader(corpus_root + '/cbio_cancer_genes', fileids=".+\\.txt")

cbio_words = list(cbio_corpus.words())
en_words = list(words.words())

def bio_chunk_features(word):
    import re
    _digits = re.compile('\d')
    word_lower = word.lower()

    cbio = word in cbio_words
    all_caps = word.isupper()
    en_word = word_lower in en_words
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

        train_set = self.get_features_from_chunk(chunked_trial)

        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def fast_calculate_features(self, words):
        import billiard
        pool = billiard.Pool(4)
        feats  = pool.map(bio_chunk_features, words)
        pool.close()
        #result = job.apply_async()
        #feats = result.get()
        return feats

    def get_features_from_chunk(self, chunks_tree):
        if chunks_tree.height()>3:
            raise Exception("Chunk tree is too deep to parse!")
        words = []
        labels = []
        for chunk in chunks_tree:
            if isinstance(chunk, nltk.Tree):
                for b in chunk:
                    words.append(b[0])
                    labels.append('BIO')
            else:
                words.append(chunk[0])
                labels.append('O')

        feats = self.fast_calculate_features(words)
        return zip(feats, labels)

    def tag(self, sentence):
        sent_tokenized = wordpunct_tokenize(sentence)
        #feats = [bio_chunk_features(word) for word in sent_tokenized]
        #feats = [pool.apply(bio_chunk_features, args=(word,)) for word in sent_tokenized]
        feats = self.fast_calculate_features(sent_tokenized)
        tags = self.classifier.classify_many(feats)
        conll = zip(sent_tokenized, tags)
        return conll

def store_pickled(classifier, root="nltk_data/classifiers", fname="biomarker_classifier.pickle"):
    import pickle
    import os
    fpath = os.path.join(root, fname)
    with open(fpath, "wb+") as f:
        pickle.dump(classifier, f)

def load_pickled(root="nltk_data/classifiers", fname="biomarker_classifier.pickle"):
    import pickle
    import os
    fpath = os.path.join(root, fname)
    c = pickle.load(file(fpath))
    return c