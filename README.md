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
* Standalone development server

    TODO

* uwsgi
    
    TODO

* nginx
    
    TODO

### Sample data pyhaukka and tests

Folder `data` contains some clinical trials downloaded from http://clinicaltrials.gov to be used while testing.

## Status

> Currently, only partial DB API of pyhaukka is implemented.

#### DB API implemented
* `get_clinical_trial_by_id`
* `insert_clinical_trial_xml`
* `search_clinical_trials`: Currently support searching by GENE names, but not yet with name expansion (e.g. searching for BRAF would not match trials with aliases such as: BRAF1, BRAF-1, P94 .. etc)

#### DB API planned
* `search_clinical_trials`: Support searching by GENE names and expand queries to aliases (e.g. from http://www.genecards.org/cgi-bin/carddisp.pl?gene=BRAF)


