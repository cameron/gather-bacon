/*! grafana - v1.5.2 - 2014-03-24
 * Copyright (c) 2014 Torkel Ödegaard; Licensed Apache License */

define(["mocks/dashboard-mock","underscore","services/filterSrv"],function(){describe("graphiteTargetCtrl",function(){var a;beforeEach(module("kibana.services")),beforeEach(module(function(a){a.value("filterSrv",{})})),beforeEach(inject(function(a,b){_targetCtrl=a({$scope:b.$new()})})),describe("init",function(){beforeEach(function(){a.add({name:"test",current:{value:"oogle"}}),a.init()})})})});