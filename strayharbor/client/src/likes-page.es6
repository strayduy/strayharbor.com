/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// External libs
const $  = require('jquery');
const _  = require('lodash');
const ko = require('knockout');
const moment = require('../bower_components/moment/moment.js');
const string_to_color = require('../bower_components/string-to-color/dist/string-to-color.umd.js');

// Components
require('./components/date-entry');

class LikesPage {
    constructor() {
        this.date_entries = ko.observableArray();
        this.page = ko.observable(1);
        this.max_pages = ko.observable(1);
        this.is_loaded = ko.observable(false);

        this.base_url = ko.observable('');
        this.init_request_params = {};

        this.page_regex = ko.pureComputed(() => {
            var base_url = this.base_url();
            return new RegExp('^' + base_url + '\/page\/(\\\d+)\/?', 'gi');
        });

        this.has_prev_page = ko.pureComputed(() => {
            return this.page() > 1;
        });

        this.has_next_page = ko.pureComputed(() => {
            return this.page() + 1 <= this.max_pages();
        });

        this.prev_page_url = ko.pureComputed(() => {
            let page = this.page();
            let base_url = this.base_url();

            if (!this.has_prev_page()) {
                return '#';
            }

            return base_url + '/page/' + (page - 1) + '/';
        });

        this.next_page_url = ko.pureComputed(() => {
            let page = this.page();
            let base_url = this.base_url();

            if (!this.has_next_page()) {
                return '#';
            }

            return base_url + '/page/' + (page + 1) + '/';
        });
    }

    init() {
        let match = this.page_regex().exec(window.location.pathname);
        this.page(match ? parseInt(match[1]) : 1);

        let params = _.assign({}, this.init_request_params, {page: this.page()});
        $.get('/date-entries.json', params)
            .done((response) => {
                let date_entries = response.date_entries;
                this.max_pages(response.max_pages);

                _.forEach(date_entries, function(date_entry) {
                    let date = moment(date_entry.date);
                    date_entry.display_date = date.format('MMMM Do, YYYY');

                    _.forEach(date_entry.likes, function(like) {
                        like.permalink = '//www.reddit.com' + like.permalink;
                        like.comments_text = like.num_comments + ' comments';
                        like.subreddit_text = '/r/' + like.subreddit;
                        like.subreddit_url = '/r/' + like.subreddit;
                        like.subreddit_color = '#' + string_to_color.getColor(like.subreddit);
                    });
                });

                this.date_entries(date_entries);
                this.is_loaded(true);
            });
    }
}

module.exports = LikesPage;
