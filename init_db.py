import logging

if __name__=='__main__':
    try:
        from config import DATABASE_URI
        from pyhaukka.db import ClinicalTrialsDatabase
        db = ClinicalTrialsDatabase(DATABASE_URI)
        db = db.connect()
        db.execute(open("schema.sql", "r").read())
    except:
        logging.exception()
