(function () {
    angular.module('haukka.trials.service.sample', ['ngResource'])
    .factory('Trials', ['$resource', function($resource){
        return $resource('sample-data/:trialId.json', {}, {
              query: {method:'GET', params:{trialId:'trials'}, isArray:true}
            });
    }]);
})();
