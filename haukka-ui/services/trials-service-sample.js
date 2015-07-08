(function () {
  'use strict';
  angular.module('haukka.trials.service', ['ngResource'])
    .factory('Trials', ['$resource', function ($resource) {
      return $resource('sample-data/:trialId.json', {trialId: '@nctid'}, {
        query: {method: 'GET', params: {trialId: 'trials'}, isArray: true}
      });
    }]);
}());
