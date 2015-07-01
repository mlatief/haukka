(function () {
    'use strict';
    
    angular.module('haukka.trials')
    .controller('TrialDetailController', ['$stateParams', 'trial', TrialDetailController]);

    function TrialDetailController($stateParams, trial){
        console.log('TrialDetailController nctid: ', $stateParams.nctid);
        console.log('Trial data:', trial.data.clinical_study);
        this.nctid = $stateParams.nctid;
        this.trial = trial.data.clinical_study;
    }

})();