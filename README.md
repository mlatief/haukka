# OncoBlocks :: haukka

> Extraction of Clinical Trials Biomarkers

haukka helps curators search clinical trials at (http://clinicaltrials.gov) for cancer biomarkers (genes and alterations), and curate them for later reuse. It started as GSoC 2015 project for OncoBlocks organization.

## pyhaukka
### Install

```sh
$ pip install
```
pyhaukka requires [PostgreSQL 9.0+](http://www.postgresql.org/) and [Python 2.7](http://python.org/) to be installed first.

#### Install PostgreSQL
1. Before running pyhaukka app, make sure PostgreSQL server is installed and properly configured.
2. Create `haukka` user and store the password at `~/.pgpass` (On Windows `%APPDATA%\postgresql\pgpass.conf`)
3. Then, using default server configurations and after running the above install command, you can run the following tests from haukka root directory to make sure all set:
```sh
$ python -m unittest tests.test_db_connection
```

### Run
* Loading clinical trials from `data/in`

```sh
$ python etl_xml_db.py
```

* Standalone development server

```sh
$ python run.py
```

* uwsgi
    
    TODO

* nginx
    
    TODO

### Sample data for tests

Folder `data` also contains some clinical trials downloaded from http://clinicaltrials.gov to be used while testing.

## Status

> * Currently, major parts of pyhaukka DB API is implemented, especially responsible for search. 
> * Requests are now wrapped with a Flask-RESTful API. 
> * Unit tests are created for both DB and Flask app.
> * Clinical Trials loader is available to load multiple xml files into the DB

#### DB API
##### Implemented and tested
* `get_clinical_trial_by_id`: Returns single trial given its NCT ID
* `insert_clinical_trial_xml`: Takes trial xml data, checksum and nctid and inserts it into `clinical_trials`` table.
* `search_clinical_trials`: Currently support searching by GENE names, but not yet with name expansion (e.g. searching for BRAF would not match trials with aliases such as: BRAF1, BRAF-1, P94 .. etc)

##### Planned
* `search_clinical_trials`: Support searching by GENE names and expand queries to aliases (e.g. from http://www.genecards.org/cgi-bin/carddisp.pl?gene=BRAF)

#### Flask-RESTful API

##### Implemented and tested
Resource URL | HTTP Verb | Functionality |
-------------| :---------: |---------------|
`/trials?q=gene_names`   | GET       | Retrieving clinical trials   |

##### Planned
Resource URL | HTTP Verb | Functionality 
-------------| :---------: |---------------
`/trials/nct_id`   | _GET_      | Retrieve a single trial
`/trials/nct_id/biomarkers`  | _GET_ | Retrieve clinical trial's biomarkers
`/trials/nct_id/biomarkers`   | _POST_ | Confirm/Add a biomarker by curator
`/trials/nct_id/biomarkers`   | _DELETE_ | Removes a biomarker by curator
`/trials`   | _POST_      | Insert new clinical trial

#### Others

##### Implemented and tested

* `etl_xml_db.py`: Module to process and load clinical trials xml files into database.

