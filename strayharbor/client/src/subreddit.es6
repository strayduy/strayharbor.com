/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const ko = require('knockout');

// Our libs
const LikesPage = require('./likes-page');

class SubredditPage extends LikesPage {
    constructor() {
        super();

        let subreddit_regex = /^\/r\/([^\/]+)(\/page\/(\d+)\/?)?/gi;
        let match = subreddit_regex.exec(window.location.pathname);
        this.subreddit = match[1];
        this.base_url('/r/' + this.subreddit);

        this.init_request_params = {subreddit: this.subreddit};
    }
}

let subreddit_page = new SubredditPage();
ko.applyBindings(subreddit_page);
subreddit_page.init();
