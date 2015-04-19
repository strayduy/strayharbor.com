/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const $  = require('jquery');
const ko = require('knockout');

// Our libs
const LikesPage = require('./likes-page');

class PostsPage extends LikesPage {
    constructor() {
        super();

        this.base_url('/posts/');

        this.init_request_params = {only_posts: true};
    }
}

let posts_page = new PostsPage();
ko.applyBindings(posts_page);
posts_page.init();
