/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const ko = require('knockout');

// Component template
const template = require('./like-entry.html');

class LikeEntry {
    constructor(params) {
        this.like = params.like;
    }
}

ko.components.register('like-entry', {
    viewModel: LikeEntry,
    template: template,
});
