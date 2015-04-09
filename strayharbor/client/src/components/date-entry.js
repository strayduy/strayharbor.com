/* jshint browserify: true */
'use strict';

// External libs
var ko = require('knockout');

// Component template
var template = require('./date-entry.html');

var DateEntry = function(params) {
    var self = this;

    self.display_date = ko.observable(params.data.display_date);
    self.likes = ko.observableArray(params.data.likes);
};

ko.components.register('date-entry', {
    viewModel: {
        createViewModel: function(params, componentInfo) {
            return new DateEntry(params);
        },
    },
    template: template,
});
