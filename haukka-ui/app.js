(function () {
  'use strict';

  // Declare app level module which depends on views, and components
  angular.module('haukka', [
    'ngSanitize',
    'ui.router',
    'haukka.trials.service', /* Use haukka.trials.service for communication with server */
    'haukka.trials',
    'haukka.widgets'
  ])
    .run(function ($rootScope, $state, $stateParams) {
      /* Provide convenient $state/$stateParams in templates and directives */
      $rootScope.$state = $state;
      $rootScope.$stateParams = $stateParams;
    })
    .config(['$stateProvider', '$urlRouterProvider',
      function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise("/");

        $stateProvider
          .state('home', {
            url: '/',
            templateUrl: 'layout/home.html',
            controller: 'HomeController as vm'
          })
          .state('about', {
            url: '/about',
            templateUrl: 'layout/about.html',
          })
          .state('trials', {
            abstract: true,
            url: '/trials',
            templateUrl: 'trials/trials.wrapper.html'
          })
          .state('trials.search', {
            url: '?query',
            resolve: {
              results: ['$stateParams', 'Trials', function ($stateParams, Trials) {
                return Trials.query({'q': $stateParams.query}).$promise;
              }]
            },
            templateUrl: 'trials/trials.list.html',
            controller: 'TrialsListController as vm'
          })
          .state('trials.detail', {
            url: '/{nctid}?highlight',
            resolve: {
              trial: ['$stateParams', 'Trials', function ($stateParams, Trials) {
                return Trials.get({'trialId': $stateParams.nctid}).$promise;
              }]
            },
            templateUrl: 'trials/trials.detail.html',
            controller: 'TrialDetailController as vm'
          });
      }]);

  angular.module('haukka.trials', []);
  angular.module('haukka.widgets', []);
}());