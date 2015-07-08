(function () {
    'use strict';
    
    angular.module('haukka.trials')
    .controller('TrialDetailController', ['$stateParams', 'trial', TrialDetailController]);

    function TrialDetailController($stateParams, trial){
        console.log('TrialDetailController nctid: ', $stateParams.nctid);
        console.log('Trial data:', trial);
        this.nctid = $stateParams.nctid;
        this.trial = trial.clinical_study;
    }

})();