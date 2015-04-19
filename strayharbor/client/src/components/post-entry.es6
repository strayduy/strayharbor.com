/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const ko = require('knockout');

// Component template
const template = require('./post-entry.html');

class PostEntry {
    constructor(params, componentInfo) {
        this.post = params.post;
    }
}

ko.components.register('post-entry', {
    viewModel: PostEntry,
    template: template,
});
