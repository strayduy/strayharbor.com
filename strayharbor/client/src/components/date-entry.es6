/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const ko = require('knockout');

// Components
require('./like-entry');
require('./post-entry');

// Component template
const template = require('./date-entry.html');

class DateEntry {
    constructor(params) {
        this.display_date = ko.observable(params.data.display_date);
        this.posts = ko.observableArray(params.data.posts);
        this.likes = ko.observableArray(params.data.likes);
    }
}

ko.components.register('date-entry', {
    viewModel: DateEntry,
    template: template,
});
