from pyhaukka.utils import init_loggers
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import logging

from pyhaukka.app import app, db
app.config.from_object('config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

init_loggers("admin.log")

def print_elapsed(start):
    import time
    cur = time.clock()
    logging.info("   {:03.2f} secs elapsed".format(cur-start))
    return cur

@manager.command
def train(corpus_path="nltk_data/corpora/clinical_trials", files=".+\\.txt",
          output="nltk_data/classifiers"):
    """
    Trains a classifier using the provided corpus and dumps the class in the output file
    """
    import time

    from nltk import Tree
    from nltk.corpus import ChunkedCorpusReader
    from pyhaukka.classify import BiomarkerClassifier, store_pickled
    try:
        cur = time.clock()
        logging.info("Reading corpus...")
        train_corpus = ChunkedCorpusReader(root=corpus_path, fileids=files)
        train_tree = Tree('S', train_corpus.chunked_words())
        cur = print_elapsed(cur)
        if train_tree:
            logging.info("Training classifier...")
            classifier = BiomarkerClassifier(train_tree)
            cur = print_elapsed(cur)

            logging.info("Dumping classifier binary...")
            store_pickled(classifier, output)
            cur = print_elapsed(cur)
        else:
            logging.error("No corpus found")
    except:
        logging.exception("Failed to load clinical trials corpus!")

if __name__ == '__main__':
    manager.run()
