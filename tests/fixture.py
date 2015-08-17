from pyhaukka.utils import convert_trial_xml_to_json


def load_sample_trials(nct_ids):
    trials = []
    for nctid in nct_ids:
        with open("data/{}.xml".format(nctid)) as ct:
            ct_xml = ct.read()
            ct_dict = convert_trial_xml_to_json(ct_xml)
            trials.append(ct_dict)
    if len(trials) < len(nct_ids):
        raise Exception("Couldn't read all test data...")
    return trials
