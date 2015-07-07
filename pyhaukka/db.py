import logging
log = logging.getLogger(__name__)

import psycopg2
from psycopg2.extras import RealDictCursor
import ujson
from datetime import datetime

from xml_dict import ConvertXmlToDict


# TODO: Improve paging performance (may be using seek instead of offset!)
#        http://leopard.in.ua/2014/10/11/postgresql-paginattion/
# TODO: Support trials tags updating
# TODO: Support users...

# Custom JSON adaptations
class uJson(psycopg2.extras.Json):
    """
    Custom psycopg2 JSON adaptation from 'Python to PostgreSQL' that uses uJson
    """
    def dumps(self, obj):
        return ujson.dumps(obj)


# Custom psycopg2JSON adaptation from PostgreSQL to Python that uses uJson
loads = lambda x: ujson.loads(x)

# Inherit from object: new style classes!
class ClinicalTrialsDatabase(object):
    conn_uri = ''
    conn = None
    def __init__(self, conn_uri=''):
        self.conn_uri = conn_uri

    def __del__(self):
        if self.conn:
            self.conn.close()

    def connect(self, conn_uri=''):
        if conn_uri:
            self.conn_uri = conn_uri
            if self.conn:
                self.close()

        if self.conn_uri and self.conn is None:
            log.debug("Connecting to PostgreSQL DB: {}".format(self.conn_uri))
            try:
                self.conn = psycopg2.connect(self.conn_uri, cursor_factory=RealDictCursor)
                self.conn.autocommit = True
                psycopg2.extras.register_json(self.conn, loads=loads)
            except:
                log.exception('Error while connecting.')
                raise
        elif not self.conn_uri:
            log.warn("Connecting to DB with empty conn_uri! Nothing actually happened!")

        return self

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def is_connected(self):
        if self.conn:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    r = cur.fetchone()
                    return len(r)>0
        else:
            return False

    def begin(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("BEGIN;")

    def commit(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("COMMIT;")

    def rollback(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("ROLLBACK;")

    def execute(self, query, **args):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)

    def query_db(self, query, args=(), one=True):
        with self.conn as conn:
            with conn.cursor() as cur:
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
        with self.conn as conn:
            with conn.cursor() as cur:
                ct_dict = ConvertXmlToDict(ct_xml_string)
                stmt = """INSERT INTO clinical_trials (nctid, ctdata, inserted, checksum)
                          VALUES (%s, %s, %s, %s)
                          RETURNING nctid;"""
                cur.execute(stmt, (nctid, uJson(ct_dict), datetime.now(), checksum))
                r = cur.fetchone()
                log.debug("... clinical trial {} inserted, checksum: {}".format(nctid, checksum))
                return r['nctid']

    def get_all_clinical_trials(self, limit=20, offset=0):
        stmt = """
        SELECT nctid, ctdata
        FROM clinical_trials
        ORDER BY nctid DESC LIMIT %s OFFSET %s;
        """
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(stmt, (limit, offset))
                r = cur.fetchall()
                log.debug("... fetched {} clinical trials!".format(len(r)))
                return r

    def search_clinical_trials(self, query, limit=20, offset=0):
        # First release just search without query expansion
        stmt = """
        SELECT nctid, ctdata, rank,
               ts_headline(ctdata->>'clinical_study', q, 'MaxFragments = 5') as headline FROM (
          SELECT nctid, ctdata, tsv, q, ts_rank_cd(tsv, q) as rank
          FROM clinical_trials, plainto_tsquery(%s) AS q
          WHERE (tsv @@ q)
        ) AS t1 ORDER BY t1.rank, t1.nctid DESC LIMIT %s OFFSET %s;
        """
        #   SELECT nctid, ctdata#>'{"clinical_study", "official_title"}' as title
        #   FROM clinical_trials
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(stmt, (query, limit, offset))
                r = cur.fetchall()
                log.debug("... clinical trials text seach with '{}' returned {} trial{}!"
                          .format(query, len(r), '' if len(r) == 1 else 's'))
                return r
