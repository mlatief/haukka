(function () {
    'use strict';
    
    angular.module('haukka.trials')
    .controller('TrialsListController', ['$stateParams','results', TrialsListController]);

    function TrialsListController($stateParams, results){
        console.log('TrialsController query: ', $stateParams.query);
        console.log('Trials count: ', results.length);
        
        this.queryString = $stateParams.query;
        this.results = results;
    }

})();