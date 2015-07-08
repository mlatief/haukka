(function () {
    angular.module('haukka.trials.service', ['ngResource'])
    .factory('Trials', ['$resource', function($resource){
        var BaseUrl = '';
        console.log('Initializing Trials service...')
        return $resource(BaseUrl + '/trials/:trialId', {trialId: '@nctid'});
    }]);
})();
