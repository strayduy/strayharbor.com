/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// ES6 polyfill
require("babel/polyfill");

// External libs
const $  = require('jquery');
const ko = require('knockout');

// Components
require('./components/post-entry');

class PostPage {
    constructor(params) {
        this.post = ko.observable();
        this.is_loaded = ko.observable(false);
    }

    init() {
        $.get(window.location.pathname + '.json')
            .done((response) => {
                this.post(response.post);
                this.is_loaded(true);
            });
    }
}

let post_page = new PostPage();
ko.applyBindings(post_page);
post_page.init();
