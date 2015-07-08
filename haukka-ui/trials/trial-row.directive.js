(function () {
  angular.module('haukka.trials')
    .directive('trialRow', function () {
      'use strict';

      return {
        templateUrl: '/trials/trial-row.directive.html',
        scope: {
          'trial': '=',
          'highlight': '='
        }
      };
    });
}());