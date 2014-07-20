angular.module("LegalEase", ['DocList', 'ngUpload'])

.constant('API_HOST', 'http://10.1.0.2:48080')

.config(function($locationProvider){
  $locationProvider.html5Mode(true);
})

.run(function(API_HOST, $rootScope){
  $rootScope.API_HOST = API_HOST;
})

.service('Url', function(API_HOST){
  var abs = function(path){
    if(path[0] != '/') path = '/' + path;
    return path;
  }

  var Url = {};
  Url.api = function(path){
    return API_HOST + abs(path);
  };
  return Url;
})
