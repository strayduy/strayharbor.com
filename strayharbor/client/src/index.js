/* jshint browserify: true */
'use strict';

// External libs
var $  = require('jquery');
var _  = require('lodash');
var ko = require('knockout');
var moment = require('moment');
var string_to_color = require('../bower_components/string-to-color/dist/string-to-color.umd.js');

// Components
require('./components/date-entry');

var IndexPage = function() {
    var self = this;

    self.date_entries = ko.observableArray();
    self.page = ko.observable(1);
    self.max_pages = ko.observable(1);
    self.is_loaded = ko.observable(false);

    self.has_prev_page = ko.pureComputed(function() {
        return self.page() > 1;
    });
    self.has_next_page = ko.pureComputed(function() {
        return self.page() + 1 <= self.max_pages();
    });

    self.prev_page_url = ko.pureComputed(function() {
        var page = self.page();

        if (!self.has_prev_page()) {
            return '#';
        }

        return '/page/' + (page - 1) + '/';
    });
    self.next_page_url = ko.pureComputed(function() {
        var page = self.page();

        if (!self.has_next_page()) {
            return '#';
        }

        return '/page/' + (page + 1) + '/';
    });

    self.init = function() {
        var page_regex = /^\/page\/(\d+)\/?/gi;
        var match = page_regex.exec(window.location.pathname);
        self.page(match ? parseInt(match[1]) : 1);

        $.get('/likes.json', {page: self.page()})
            .done(function(response) {
                var date_entries = response.date_entries;
                self.max_pages(response.max_pages);

                _.forEach(date_entries, function(date_entry) {
                    var date = moment(date_entry.date);
                    date_entry.display_date = date.format('MMMM Do, YYYY');

                    _.forEach(date_entry.likes, function(like) {
                        like.permalink = '//www.reddit.com' + like.permalink;
                        like.comments_text = like.num_comments + ' comments';
                        like.subreddit_text = '/r/' + like.subreddit;
                        like.subreddit_url = '//www.reddit.com/r/' + like.subreddit;
                        like.subreddit_color = '#' + string_to_color.getColor(like.subreddit);
                    });
                });

                self.date_entries(date_entries);
                self.is_loaded(true);
            });
    };
};

var index_page = new IndexPage();
ko.applyBindings(index_page);
index_page.init();
