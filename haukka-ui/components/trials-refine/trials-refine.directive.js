(function () {
    angular.module('haukka.trials')
    .directive('trialsRefine', function(){
        'use strict';
        
        return {
            templateUrl: 'components/trials-refine/trials-refine.directive.html',
            scope: {
                filterHeading:'@'
            },
            controllerAs: 'refctrl',
            controller: function(){
                console.log(this.heading);
            }
        };
    })
})();