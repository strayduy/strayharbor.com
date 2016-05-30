import Vue from 'vue';
import VueResource from 'vue-resource';
import VueRouter from 'vue-router';
import DateEntries from './date-entries.vue';

Vue.use(VueResource);
Vue.use(VueRouter);

let App = Vue.extend({});
let router = new VueRouter({history: true});

// Scroll to the top of the page when we change pages
router.beforeEach(function(transition) {
    window.scrollTo(0, 0);
    transition.next();
});

router.map({
    '/': {
        name: 'all',
        component: DateEntries,
    },
    '/page/:page': {
        name: 'all_paginated',
        component: DateEntries,
    },
    '/r/:subreddit': {
        name: 'subreddit',
        component: DateEntries,
    },
    '/r/:subreddit/page/:page': {
        name: 'subreddit_paginated',
        component: DateEntries,
    },
});

router.start(App, 'body');
