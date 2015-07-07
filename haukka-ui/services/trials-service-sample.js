(function () {
    angular.module('haukka.trials.service.sample', [])
    .service('TrialsService', ['$http', '$q', function($http){
        var _service = this;

        this.searchTrials = function(q){
            if(!q){
                console.log("reject the undefined query!", q);
                return $q.reject('No query string defined!');
            }

            console.log("calling searchTrials with: ", q);
            return $http.get('sample-data/trials.json');
        }

        this.getTrial = function(id){
            console.log("calling getTrial with: ", id);
            return $http.get('sample-data/trial0001.json');
        }
    }]);
})();
