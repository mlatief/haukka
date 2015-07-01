(function () {
    'use strict';
    
    angular.module('haukka.trials')
    .controller('TrialsListController', ['$stateParams','trials', TrialsListController]);

    function TrialsListController($stateParams, trials){
        console.log('TrialsController query: ', $stateParams.query);
        console.log('Trials count: ', trials.data.length);
        
        this.queryString = $stateParams.query;
        this.trials = trials.data;
    }

})();