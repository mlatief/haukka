# OncoBlocks :: haukka

> Extraction of Clinical Trials Biomarkers

haukka helps curators search clinical trials at (http://clinicaltrials.gov) for cancer biomarkers (genes and alterations), and curate them for later reuse. It started as GSoC 2015 project for OncoBlocks organization.

## pyhaukka
[![Build Status](https://travis-ci.org/mlatief/haukka.svg?branch=pyhaukka-experiment)](https://travis-ci.org/mlatief/haukka)

### Installing with Vagrant

pyhaukka requires [PostgreSQL 9.4](http://www.postgresql.org/) and [Python 2.7](http://python.org/) to be installed first. In this project we are using Vagrant to manage a VirtualBox instance. So first install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).

Then fire up a ubuntu/trusty64 instance, and will install required packages: PostgreSQL 9.4, Python 2.7, pip and virtualenv.

```sh
$ vagrant up
$ vagrant ssh
...
Host: 127.0.0.1
Port: 2222
Username: vagrant
...
```

After the instance is up and running, SSH to the mentioned port and then while at the home directory:

```sh
$ virtualenv env
Installing setuptools, pip, wheel...done.

$ source env/bin/activate
$ cd /vagrant/
$ pip install -r requirements.txt
$ py.test tests
```

Note that the directory `/vagrant/` inside the virtual box is synced with the project folder at the host (this repository).

### Run

Currently there are two main modules in the project: `pyhaukka` and `load_trials.py`.

* Running a WSGI server
```sh
$ python wsgi.py
```

Or, using [uWSGI](https://github.com/unbit/uwsgi):

```sh
$ uwsgi uwsgi.ini
```

* Loading clinical trials from `./data/in`
```sh
$ python load_trials.py
```

This process will look for new `NCTxxx.xml` files in `./data/in/` and process them sequentially, and move the processed files to `./data/out/` while inserting the trials into the DB. If the process encountered an error processing one file it is moved to `./data/err/`.

### Sample data for tests

Folder `data` contains some clinical trials downloaded from http://clinicaltrials.gov to be used while testing.

## Status

> * Currently, major parts of pyhaukka DB API is implemented, especially the part responsible for search. 
> * Requests are now wrapped with a Flask-RESTful API. 
> * Unit tests are created for both DB and Flask app.
> * Clinical Trials loader is available to load multiple xml files into the DB
> * Static files are being served smartly (cache ready, gzipped .. etc) using WhiteNoise
> * Continous integration using TravisCI
> * Vagrant development environments

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
`/trials`   | _POST_      | Insert new clinical trial
`/trials/nct_id`   | _GET_      | Retrieve a single trial
`/trials/nct_id/biomarkers?type=gner|curator|all`  | _GET_ | Retrieve clinical trial's biomarkers
`/trials/nct_id/biomarkers`   | _POST_ | Add a biomarker by curator 
`/trials/nct_id/biomarkers/<bio_marker_slug>`  | _GET_ | Retrieve details about biomarker.
`/trials/nct_id/biomarkers/<bio_marker_slug>`  | _POST_ | Change biomarker type.
`/trials/nct_id/biomarkers/<bio_marker_slug>`  | _DELETE_ | Removes a biomarker.
`/trials/nct_id/biomarkers`  | _GET_ | Retrieve clinical trial's biomarkers.

#### Others

##### Implemented and tested

* `load_trials.py`: Module to process and load clinical trials xml files into database.

