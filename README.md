# OncoBlocks :: haukka

> Extraction of Clinical Trials Biomarkers

*haukka* helps curators search clinical trials at (http://clinicaltrials.gov) for cancer biomarkers (genes and alterations), and curate them for future reference. *haukka* started as GSoC 2015 project for OncoBlocks organization.

## pyhaukka
[![Build Status](https://travis-ci.org/mlatief/haukka.svg?branch=master)](https://travis-ci.org/mlatief/haukka)

### Installing with Vagrant

#### Prerequisites:
pyhaukka depends on:
- [PostgreSQL 9.4](http://www.postgresql.org/)
- [Redis](http://redis.io/)
- [Python 2.7](http://python.org/)

In this project [Vagrant](https://www.vagrantup.com/) is used to manage a [VirtualBox](https://www.virtualbox.org/) instance for development. So just start by installing these tools, then fire up the ubuntu/trusty64 instance, which will also install required packages: PostgreSQL 9.4, redis, Python 2.7, pip and virtualenv and create required setup on a virtual box image.
t
```sh
$ vagrant up
$ vagrant ssh
...
Host: 127.0.0.1
Port: 2222
Username: vagrant
...
```

After the instance is up and running, SSH to the mentioned port and then:

```sh
$ cd /vagrant/
$ py.test tests
```

Note that the directory `/vagrant/` inside the virtual box is synced with the project folder at the host (this repository).

### Training the classifier

1. Provide training corpus in `nltk_data/corpora/clinical_trials` directory. It should look something like this

```
Crizotinib in Pretreated Metastatic Non-small-cell Lung Cancer With [MET] Amplification.
within the same liver segment as long as the dose constraints to normal tissue can be met.
This is a Phase II, open-label, non-randomized, multi-center study of oral Dabrafenib in
combination with oral Trametinib in subjects with rare cancers including anaplastic thyroid
cancer, biliary tract cancer, gastrointestinal stromal tumor, non-seminomatous germ cell
tumor/non-geminomatous germ cell tumor, hairy cell leukemia, World Health Organization (WHO)
Grade 1 or 2 glioma, WHO Grade 3 or 4 (high-grade) glioma, multiple myeloma, and
adenocarcinoma of the small intestine, with [BRAF V600E] positive-mutations. This study is
designed to determine the overall response rate (ORR) of oral Dabrafenib in combination with
oral Trametinib in subjects with rare [BRAF V600E] mutated cancers. Subjects will need to have
a fresh or frozen tumor tissue sample provided to confirm the [BRAF V600E] mutation status.
Only subjects with histologically confirmed advanced disease and no available standard
treatment options will be eligible for enrollment. Subjects will undergo screening
assessments within 14 days (up to 35 days for ophthalmology exam, echocardiogram or disease
assessments) prior to the start of treatment to determine their eligibility for enrollment
in the study.
```

Note the brackets around the words that should be tagged as biomarkers.

2. Train a classifier and store it

```
python manage.py train
```

3. After this step a classifier binary should be stored in `nltk_data/classifiers/biomarker_classifier.pickle` and will be picked up by default by the RESTful webservice.

### Run the webservice

* Start Celery worker

Before the webservice can dispatch requests, background worker need to be started.

```
celery worker -A pyhaukka.worker
```

Note: on the provided Vagrant instance a redis-server is installed and started using the default configuration.

* Running a development WSGI server

Then either to run a WSGI server for debugging

```sh
$ python wsgi.py
```

Or, using [uWSGI](https://github.com/unbit/uwsgi):

```sh
$ uwsgi uwsgi.ini
```

### Webservice RESTful API

Resource URL | HTTP Verb | Functionality |
-------------| :---------: |---------------|
`/trials`   | _GET_      | Get list of stored trials
`/trials/nct_id`   | _GET_      | Retrieve a single trial detail
`/tasks`   | _POST_      | Post a new task to load and process a trial
`/tasks/task_id`   | _GET_      | Retrieve task result and status

#### Tasks endpoint
- Requests to process single trials can be sent to background worker, by sending a POST request to /tasks endpoint with the URL of the clinical trial. e.g:

```
POST /tasks
{"url":"https://clinicaltrials.gov/show/NCT02034110?displayxml=true"}
```

This will enqueue the clinical trial to be fetched, and then run the classifier on it. To see the results, use `trials` endpoint

- To query the result and status of a task use `/tasks/<task_id>` endpoint:

```
GET /tasks/9ea876aa-17c6-493d-8178-461bfd330a80
{
    "result": "NCT02034110", 
    "state": "SUCCESS", 
    "status": "Trial processed!"
}
```

#### Trials endpoint
- GET requests to `/trials` list all the currently stored and processed trials

- GET request to specific `/trials/<NCT_ID>`, fetches the stored trial data as well as the results of running the classifier

```
GET /trials/NCT02034110
{
  "nct_id":"NCT02034110",
  "ner_result":[["BRAF","BIO"],["V600E","BIO"],["BRAF","BIO"],["V600E","BIO"],["ORR","BIO"],["BRAF","BIO"],["V600E","BIO"],["BRAF","BIO"],["V600E","BIO"],["ECOG","BIO"],["BRAF","BIO"],["V600E","BIO"],["BRAF","BIO"],["CLIA","BIO"],["BRAF","BIO"],["BRAF","BIO"],["CLIA","BIO"],["BRAF","BIO"],["GSK","BIO"],["FFPE","BIO"],["GSK","BIO"],["BRAF","BIO"],["MEK","BIO"],["ASCT","BIO"],["ABMT","BIO"],["PBSCT","BIO"],["GSK","BIO"],["MRI","BIO"],["GSK","BIO"],["CNS","BIO"],["RVO","BIO"],["CSR","BIO"],["RVO","BIO"],["CSR","BIO"],["RVO","BIO"],["CSR","BIO"],["RVO","BIO"],["CSR","BIO"],["NYHA","BIO"],["LVEF","BIO"],["LLN","BIO"],["LLN","BIO"],["LVEF","BIO"],["INR","BIO"],["HBV","BIO"],["HCV","BIO"],["RNA","BIO"],["HIV","BIO"],["BRAF","BIO"],["V600E","BIO"]],
  "processed_on":null,
  "trial":
    {"brief_summary":"\n      This is a Phase II, open-label, non-randomized, multi-center study of oral Dabrafenib in\n      combination with oral Trametinib in subjects with rare cancers including anaplastic thyroid\n      cancer, biliary tract cancer, gastrointestinal stromal tumor, non-seminomatous germ cell\n      tumor/non-geminomatous germ cell tumor, hairy cell leukemia, World Health Organization (WHO)\n      Grade 1 or 2 glioma, WHO Grade 3 or 4 (high-grade) glioma, multiple myeloma, and\n      adenocarcinoma of the small intestine, with BRAF V600E positive-mutations. This study is\n      designed to determine the overall response rate (ORR) of oral Dabrafenib in combination with\n      oral Trametinib in subjects with rare BRAF V600E mutated cancers. Subjects will need to have\n      a fresh or frozen tumor tissue sample provided to confirm the BRAF V600E mutation status.\n      Only subjects with histologically confirmed advanced disease and no available standard\n      treatment options will be eligible for enrollment. Subjects will undergo screening\n      assessments within 14 days (up to 35 days for ophthalmology exam, echocardiogram or disease\n      assessments) prior to the start of treatment to determine their eligibility for enrollment\n      in the study.\n    ","condition":["Cancer"],"criteria":"\n        Inclusion Criteria:\n\n          -  Signed, written informed consent.\n\n          -  Sex: male or female.\n\n          -  Age: >=18 years of age at the time of providing informed consent.\n\n          -  Eastern Cooperative Oncology Group (ECOG) performance status: 0, 1 or 2.\n\n          -  BRAF V600E mutation-positive tumor: Local testing - Local BRAF mutation test results\n             obtained by a Clinical Laboratory Improvement Amendments (CLIA) approved local\n             laboratory may be used to permit enrollment of subjects with positive results. Local\n             BRAF mutation test results will be subject to central verification; Central testing -\n             Local BRAF mutation test results will be confirmed by central testing in a CLIA\n             approved, designated central reference laboratory by the THxID BRAF assay or an\n             alternate GSK designated assay. NOTE: For central testing, Formalin-fixed\n             paraffin-embedded (FFPE) core bone marrow (BM) biopsies are not acceptable from\n             subjects in the Multiple myeloma (MM) cohort.\n\n          -  Able to swallow and retain orally administered medication. NOTE: Subject should not\n             have any clinically significant gastrointestinal (GI) abnormalities that may alter\n             absorption such as malabsorption syndrome or major resection of the stomach or\n             bowels. For example, subjects should have no more than 50% of the large intestine\n             removed and no sign of malabsorption (i.e., diarrhea).NOTE: If clarification is\n             needed as to whether a condition will significantly affect the absorption of study\n             treatments, contact the GSK Medical Monitor.\n\n          -  Female Subjects of Childbearing Potential:  Subjects must have a negative serum\n             pregnancy test within 7 days prior to the first dose of study treatment and agrees to\n             use effective contraception, throughout the treatment period and for 4 months after\n             the last dose of study treatment.\n\n          -  French subjects: In France, a subject will be eligible for inclusion in this study\n             only if either affiliated to or a beneficiary of a social security category.\n\n        Exclusion Criteria:\n\n          -  Prior treatment with: BRAF and/or MEK inhibitor(s); anti-cancer therapy (e.g.,\n             chemotherapy with delayed toxicity, immunotherapy, biologic therapy or\n             chemoradiation) within 21 days (or within 42 days if prior nitrosourea or mitomycin C\n             containing therapy) prior to enrollment and/or daily or weekly chemotherapy without\n             the potential for delayed toxicity within 14 days prior to enrolment; Investigational\n             drug(s) within 30 days or 5 half-lives, whichever is longer, prior to enrollment\n\n          -  Previous major surgery within 21 days prior to enrollment.\n\n          -  Prior extensive radiotherapy treatment within 21 days prior to enrolment. NOTE:\n             Limited radiotherapy for palliative care is permitted within 14 days prior to\n             enrollment as long as any radiation-related toxicity has resolved prior to\n             enrollment.\n\n          -  Prior solid organ transplantation or allogenic stem cell transplantation (ASCT).\n             NOTE: Previous autologous bone marrow transplant (ABMT) or autologous peripheral\n             blood stem cell transplant (PBSCT) is permitted.\n\n          -  History of: Interstitial lung disease or pneumonitis; Another malignancy. NOTE:\n             Subjects with another malignancy are eligible if: (a) disease-free for 3 years, (b)\n             had a history of completely resected non-melanoma skin cancer, and/or (c) have a\n             indolent second malignancy(ies) defined as a slow growing second/concurrent\n             malignancy which is characterized by slow growth, a high initial response rate and a\n             relapsing , progressive disease course. For example, a previously untreated low grade\n             and select intermediate-grade lymphoid malignancy would be allowed as per the\n             available body of evidence. There are no available clinical alternatives to the\n             proposed population. Consult a GSK Medical Monitor if unsure whether second\n             malignancies meet requirements specified above.\n\n          -  Presence of: cerebral metastases (except for subjects in the WHO Grade 1 or 2 Glioma\n             or WHO Grade 3 or 4 Glioma histology cohorts). NOTE: Subjects with brain metastases\n             may be included if: All known lesions have been previously treated with surgery or\n             stereotactic radiosurgery, and Any remaining cerebral lesion(s) are asymptomatic and\n             confirmed stable disease (i.e., no increase in lesion size) for >=90 days prior to\n             enrollment as documented by two consecutive magnetic resonance imaging (MRI) or\n             computed tomography (CT) scans with contrast, and No treatment with corticosteroids\n             or enzyme-inducing anticonvulsants required for >=30 days prior to enrolment.\n             Approval received from GSK Medical Monitor.\n\n          -  Presence of symptomatic or untreated leptomeningeal or spinal cord compression. NOTE:\n             Subjects who have been previously treated for these conditions and have stable\n             central nervous system (CNS) disease (documented by consecutive imaging studies) for\n             >60 days, are asymptomatic and currently not taking corticosteroids, or have been on\n             a stable dose of corticosteroids for at least 30 days prior to enrollment, are\n             permitted.\n\n          -  Presence of pre-existing >= Grade 2 peripheral neuropathy.\n\n          -  Presence of unresolved treatment-related toxicity of >= Grade 2 (except alopecia) or\n             toxicities listed in the general and histology-specific adequate organ function\n             tables at the time of enrolment.\n\n          -  Presence of any serious and/or unstable pre-existing medical disorder (aside from\n             malignancy exception above), psychiatric disorder, or other conditions that could\n             interfere with subject's safety, obtaining informed consent or compliance to the\n             study procedures.\n\n          -  History or current evidence/risk of retinal vein occlusion (RVO) or central serous\n             retinopathy (CSR): History of RVO or CSR, or predisposing factors to RVO or CSR\n             (e.g., uncontrolled glaucoma or ocular hypertension, uncontrolled systemic disease\n             such as hypertension or diabetes mellitus, or history of hyperviscosity or\n             hypercoagulability syndromes); Visible retinal pathology as assessed by ophthalmic\n             examination that is considered a risk factor for RVO or CSR such as evidence of new\n             optic disc cupping, evidence of new visual field defects and intraocular pressure >21\n             mmHg.\n\n          -  History or evidence of cardiovascular risk including any of the following: Acute\n             coronary syndromes (including myocardial infarction and unstable angina), coronary\n             angioplasty, or stenting within 6 months prior to enrolment; Clinically significant\n             uncontrolled arrhythmias NOTE: Subjects with controlled atrial fibrillation for >30\n             days prior to enrollment are eligible; Class II or higher congestive heart failure as\n             defined by the New York Heart Association (NYHA) criteria; Left ventricular ejection\n             fraction (LVEF) below the institutional lower limit of normal (LLN). NOTE: If a LLN\n             does not exist at an institution, then use LVEF <50%.; Corrected QT (QTc) interval\n             for heart rate using Bazett-corrected QT interval (QTcB) >=480 millisecond (msec);\n             Intracardiac defibrillator and/or permanent pacemaker; Treatment-refractory\n             hypertension defined as a blood pressure (BP) >140/90 millimeters of mercury (mmHg)\n             which may not be controlled by anti-hypertensive medication(s) and/or lifestyle\n             modifications; Known cardiac metastases.\n\n          -  Current use of prohibited medication(s) or requirement of prohibited medications\n             during study. NOTE: Use of anticoagulants such as warfarin is permitted; however,\n             international normalization ratio (INR) must be monitored according with local\n             institutional practice.\n\n          -  Positive for: Hepatitis B surface antigen or Hepatitis C antibody. NOTE: Subjects\n             with laboratory evidence of cleared hepatitis B virus (HBV) and hepatitis C virus\n             (HCV) infection will be permitted. NOTE: False positive subjects may be cleared for\n             enrollment based on RNA-based assays; Human immunodeficiency virus (HIV); testing not\n             required.\n\n          -  Known immediate or delayed hypersensitivity reaction or idiosyncrasy to drugs\n             chemically related to study treatment, or excipients, or to dimethyl sulfoxide and/or\n             sulfonamides (structural component of dabrafenib).\n\n          -  Female subjects: Pregnant, lactating or actively breastfeeding.\n\n          -  Subjects enrolled in France: The French subject has participated in any study using\n             an investigational product (IP) within 30 days prior to enrollment in this study.\n      ",
    "detailed_description":null,
    "keywords":["trametinib","Dabrafenib","solid tumors","BRAF V600E mutation","efficacy","safety"],
    "lastchanged_date":"July 23, 2015",
    "location":["United States","Austria","Belgium","Canada","Denmark","France","Germany","Italy","Korea, Republic of","Netherlands","Norway","Sweden"],
    "nct_id":"NCT02034110",
    "overall_status":"Recruiting",
    "title":"A Phase II, Open-label, Study in Subjects With BRAF V600E-Mutated Rare Cancers With Several Histologies to Investigate the Clinical Efficacy and Safety of the Combination Therapy of Dabrafenib and Trametinib"}
}
```

### Data model
Trial data is stored in PostgreSQL database for further retrieval by search queries.

Attribute | Description
:--------:|:-----------
`nctid` | e.g `NCT02034110`
`url` | e.g. https://clinicaltrials.gov/show/NCT02034110?displayxml=true
`trial_data` | JSON dictionary of clinical trial data <sup>1</sup>
`overall_status` | Overall status as read from clinical trial XML
`ner_result` | JSON dictionary of extracted biomarkers <sup>1</sup>
`lastchanged_date` | Lastchanged date of the clinical trial found in the XML
`loaded_on` | When the trial is loaded

> <sup>1</sup> JSON for trial_data and ner_result is what is similar to those mentioned earlier


### Features set and NaiveBayesClassifier 
The following features are calculated for each word to classify a word as being part of a biomarker or not.

  - `cbio`: Binary feature, True if the word exists in `cbio_cancer_genes` list.
  - `all_caps`: Binary feature, True if the word is all CAPS.
  - `en_word`: Binary feature, True if the word is an English word.
  - `stop_word`: Binary feature, True if the word is among NLTK list of stop words.
  - `has_digits`: Binary feature, True if the word contains some digits.
  - `all_digits`: Binary feature, True if the word is completely a digital number.
  - `word_len`: Length of the word to be tagged.
  - `tag`: The word is tagged either `BIO` if it is part of a biomarker or `O` if not.

Examples:

Word | cbio | all_caps | en_word | stop_word | has_digits | all_digits | word_len | tag (training) 
-----|:----:|:--------:|:-------:|:---------:|:----------:|:----------:|:--------:|:----------------:
written | No | No | Yes | No | No | No | 7 | O 
documentation | No | No | Yes | No | No | No | 13 | O 
of | No | No | Yes | Yes | No | No | 2 | O 
BRAF | Yes | Yes | No | No | No | No | 4 | BIO 
V600 | No | Yes | No | No | Yes | No | 4 | BIO 
mutation | No | No | Yes | No | No | No | 8 | O 
This | No | No | Yes | Yes | No | No | 4 | O 
is | No | No | Yes | Yes | No | No | 2 | O
a  | No | No | Yes | Yes | No | No | 1 | O
Phase | No | No | Yes | No | No | No | 5 | O
II | No | No | No | No | No | No | 2 | O
open | No | No | Yes | No | No | No | 4 | O
label | No | No | Yes | No | No | No | 5 | O
non | No | No | Yes | Yes | No | No | 3 | O
randomized | No | No | Yes | Yes | No | No | 10 | O
multi | No | No | Yes | No | No | No | 5 | O
center | No | No | Yes | No | No | No | 6 | O
study | No | No | Yes | No | No | No | 5 | O
