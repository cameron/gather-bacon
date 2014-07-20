angular.module('DocList', [])

.service('DocList', function($http, Url){
  return function(){
    return $http.get(Url.api('docs'));
  }
})

.controller('DocListCtrl', function($scope, DocList, API_HOST, $sce, $window){
  $scope.uploadUrl = $sce.trustAsResourceUrl(API_HOST + '/upload');
  DocList().success(function(res){
    $scope.docs = res.data;
  });
  $window.addEventListener('message', function(event) {
    $scope.$apply(function() {
      $scope.docs.push(JSON.parse(event.data).data);
    });
  });
})

.directive('docList', function(){
  return {
    restrict: 'E',
    templateUrl: 'modules/doc-list/doc-list.html',

  }
})