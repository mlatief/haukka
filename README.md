# OncoBlocks :: haukka

The project aims to help curators search [clinicaltrials.gov](clinicaltrials.gov) for trials matching different biomarkers, especially cancer genes and their mutations.

## The UI based on AngularJS 

### Install

Bower is used to fetch and install Haukka's UI JavaScript dependencies. `bower.json` manifest file includes the dependencies and can be used with `bower` script as following:

```sh
$ bower install
```

### Run & Preview

The UI is an AngularJS application that is runnable using a webserver starting at `app` directory. For example to install and start [`http-server`](https://github.com/indexzero/http-server) locally :

```sh
$ npm install http-server -g
$ cd app
$ http-server
Starting up http-server, serving ./ on: http://0.0.0.0:8080
Hit CTRL-C to stop the server

```

Then you can browse the application at `http://localhost:8080`.

### Sample data

Initial sample data is statically loaded from files `app/sample-data/trials.json` and `app/sample-data/trials.json`. They are currently loaded by `trials-service-sample.js` to aid with debugging and development of the UI.

## Status

> Currently, the application doesn't perform much. Rather, it is a skeleton of AngualrJS based UI which should be easily extendable. While every care has been taken to follow the latest AngularJS style guides, especially: https://github.com/johnpapa/angular-styleguide and https://github.com/mgechev/angularjs-style-guide, still some legacy practices found their way to this commit.
