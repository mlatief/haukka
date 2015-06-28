import psycopg2
from psycopg2.extras import DictCursor
from utils import init_logger
import ujson
from datetime import datetime

from xml_dict import ConvertXmlToDict

DEFAULT_DB_NAME = 'haukka'
DEFAULT_USER = 'haukka'
# Password is retrieved by libpq from .pgpass file (on Windows %APPDATA%\postgresql\pgpass.conf)

log = init_logger(__name__)

# Custom JSON adaptations
class uJson(psycopg2.extras.Json):
    '''
    Custom psycopg2 JSON adaptation from 'Python to PostgreSQL' that uses uJson
    '''
    def dumps(self, obj):
        return ujson.dumps(obj)


# Custom psycopg2JSON adaptation from PostgreSQL to Python that uses uJson
loads = lambda x: ujson.loads(x)

class ClinicalTrialsDatabase(object):
    def __init__(self, conn_uri=''):
        if not conn_uri:
            conn_uri = "dbname='{}' user='{}'".format(DEFAULT_DB_NAME, DEFAULT_USER)
        log.info("Connecting to PostgreSQL DB: {}".format(conn_uri))
        self.conn = psycopg2.connect(conn_uri, cursor_factory=DictCursor)
        self.conn.autocommit = True
        psycopg2.extras.register_json(self.conn, loads=loads)
        log.info("... connected, ujson registered, cursor_factory=DictCursor"
                      ", autocommit {}".format(self.conn.autocommit))

    def execute(self, query, **args):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, args)


    def query_db(self, query, args=(), one=True):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, args)
                if one:
                    rv = cur.fetchone()
                else:
                    rv = cur.fetchall()

                return rv

    def get_clinical_trial_by_id(self, nct_id):
        stmt = "SELECT * FROM clinical_trials WHERE nctid = %s"
        r = self.query_db(stmt, (nct_id,))
        return r

    def insert_clinical_trial_xml(self, nctid, ct_xml_string, checksum):
        with self.conn:
            with self.conn.cursor() as cur:
                ct_dict = ConvertXmlToDict(ct_xml_string)
                stmt = """INSERT INTO clinical_trials (nctid, ctdata, inserted, checksum)
                          VALUES (%s, %s, %s, %s)
                          RETURNING nctid;"""
                cur.execute(stmt, (nctid, uJson(ct_dict), datetime.now(), checksum))
                r = cur.fetchone()
                log.debug("... clinical trial {} inserted, checksum: {}".format(nctid, checksum))
                return r[0]

    # GNER Tags: [{'ne': '<named entity>', 'type': '<gene, drug, alteration ...>'}, ... ]
    def append_gner_tags_to_clinical_trial(self, nctid, tags):
        pass

    def remove_all_gner_tags_from_clinical_trial(self, nctid):
        with self.conn:
            with self.conn.cursor() as cur:
                stmt = "UPDATE clinical_trials SET gner_tagged = [] WHERE nctid = %s"
                cur.execute(stmt, (nctid,))
                log.warn("... clinicatl trial {} inserted, checksum: {}"
                             .format(nctid))

    def set_clinical_trial_rank(self, nctid, rank):
        pass

    # Curator Tags: [{'curator': '<curator name>', 'tag': '<tag data>'}, ... ]
    def append_curator_tags_to_clinical_trial(self, nctid, tags):
        pass

    def remove_all_curator_tags_from_clinical_trial(self, nctid):
        pass

    def get_list_of_clinical_trials(self, tags):
        pass
