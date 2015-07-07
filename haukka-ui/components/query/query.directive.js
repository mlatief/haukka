(function () {
    angular.module('haukka.widgets')
    .directive('query', function(){
        'use strict';
        
        return {
            templateUrl: 'components/query/query.directive.html',
            scope: {
                queryString: '='
            },
            bindToController: true,
            controllerAs: 'vm',
            controller: ['$state', QueryController]
        };
    });

    function QueryController($state){
        //console.log(this.queryString);
        this.search = function(){
            console.log('directive search: ', this.queryString);
            $state.go('trials.search', {query: this.queryString})
        }
    }
})();