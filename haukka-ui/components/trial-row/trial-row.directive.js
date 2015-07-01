(function () {
    angular.module('haukka.trials')
    .directive('trialRow', function(){
        'use strict';
        
        return {
            templateUrl: 'components/trial-row/trial-row.directive.html',
            scope: {
                'trial': '='
            }
        };
    })
})();