import xml.etree.ElementTree as ET
import hashlib
import os
import shutil
from datetime import datetime

from pyhaukka.db import ClinicalTrialsDatabase
from utils import init_loggers

log = init_loggers(log_file='load_trials.log')

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
    if not os.path.exists('data/in'):
        log.error("Can't find data/in directory!")
        return

    if not os.path.exists('data/err'):
        log.error("Can't find data/err directory!")
        return

    if not os.path.exists('data/out'):
        log.error("Can't find data/out directory!")
        return

    log.info("Processing data/in directory...")
    for f in os.listdir('data/in'):
        file_path = 'data/in/{}'.format(f)
        try:
            log.info("Processing {} ...".format(f))
            if f.lower().endswith('.xml'):
                load_trial_xml(file_path)
                valid_count = valid_count + 1
                log.debug("... successfully processed, moving {} to data/out directory...".format(f))
                shutil.move(file_path, 'data/out')
            elif f.lower().endswith('.zip') or f.lower().endswith('.gz'):
                log.warn("... compressed files aren't supported yet")
            else:
                log.warn("... unsupported file {}".format(f))
        except Exception as ex:
            log.exception("... error processing {}, moving to data/err directory...".format(f))
            shutil.move(file_path, 'data/err/{}.{}'.format(f, datetime.now().strftime("%Y%m%d-%H%M%S")))
            error_count = error_count + 1

    log.info("Processed {} files.. valid: {} , error: {}".format(valid_count+error_count, valid_count, error_count))

if __name__ == '__main__':
    process_new_files()