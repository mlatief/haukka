'use strict';

// Declare app level module which depends on views, and components
angular.module('haukka', [
  'ui.router',
  'haukka.trials',
  'haukka.widgets',
  'haukka.trials.service.sample' /* Use haukka.trials.service for communication with server */
])
.run(function ($rootScope, $state, $stateParams) {
  /* Provide convenient $state/$stateParams in templates and directives */
  $rootScope.$state = $state;
  $rootScope.$stateParams = $stateParams;
})
.config(['$stateProvider', '$urlRouterProvider', 
  function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/");

  $stateProvider
  .state('home', {
    url:'/',
    templateUrl: 'layout/home.html',
    controller: 'HomeController as vm'
  })
  .state('about', {
    url:'/about',
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
      trials: ['$stateParams', 'TrialsService', function($stateParams, TrialsService){
        return TrialsService.searchTrials($stateParams.query);
      }]
    },
    templateUrl: 'trials/trials.list.html',
    controller: 'TrialsListController as vm'
  })
  .state('trials.detail', {
      url:'/{nctid}',
      resolve: {
        trial: ['$stateParams', 'TrialsService', function($stateParams, TrialsService){
          return TrialsService.getTrial($stateParams.nctid);
        }]
      },
      templateUrl: 'trials/trials.detail.html',
      controller: 'TrialDetailController as vm'
    })
  ;
}]);

angular.module('haukka.trials', []);
angular.module('haukka.widgets', []);