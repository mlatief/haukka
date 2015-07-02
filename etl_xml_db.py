import xml.etree.ElementTree as ET
import hashlib
import os, shutil
from datetime import datetime

from pyhaukka.db import ClinicalTrialsDatabase
from pyhaukka.utils import init_logger

log = init_logger(__name__)

def load_trial_xml(file_name):
    db = ClinicalTrialsDatabase()
    with open(file_name, "r") as ct:
        ct_xml = ct.read()

        m = hashlib.md5()
        m.update(ct_xml)
        ct_checksum = m.hexdigest()

        root = ET.fromstring(ct_xml)
        nctid = root.findtext('.//nct_id')
        db.insert_clinical_trial_xml(nctid, ct_xml, ct_checksum)

def process_new_files():
    valid_count = 0
    error_count = 0
    print "Processing data/in directory..."
    for f in os.listdir('data/in'):
        file_path = 'data/in/{}'.format(f)
        try:
            log.info("Processing {} ...".format(f))
            if f.endswith('.xml'):
                load_trial_xml(file_path)
                valid_count = valid_count + 1
                log.info("... successfully processed, moving {} to data/out directory...".format(f))
            elif f.endswith('.zip') or f.endswith('.gz'):
                log.warn("... compressed files aren't supported yet")
            shutil.move(file_path, 'data/out')
        except Exception as ex:
            log.exception("... error processing {}, moving to data/err directory...".format(f))
            shutil.move(file_path, 'data/err/{}.{}'.format(f, datetime.now().strftime("%Y%m%d-%H%M%S")))
            error_count = error_count + 1

    print "Processed {} files.. valid: {} , error: {}".format(valid_count+error_count, valid_count, error_count)

if __name__ == '__main__':
    process_new_files()