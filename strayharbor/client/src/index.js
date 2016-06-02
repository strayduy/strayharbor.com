// Third party libs
import Vue from 'vue';
import VueResource from 'vue-resource';
import VueRouter from 'vue-router';

// Third party CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';

// Our libs
import DateEntries from './date-entries.vue';

// Our CSS
import './common.css';

// Load Vue plugins
Vue.use(VueResource);
Vue.use(VueRouter);

// Initialize app and router
let App = Vue.extend({});
let router = new VueRouter({history: true});

// Scroll to the top of the page when we change pages
router.beforeEach(function(transition) {
    window.scrollTo(0, 0);
    transition.next();
});

// Routes
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

// Bind app to the document body
router.start(App, 'body');

// The document body is initially hidden while the app loads. Once it's loaded,
// show the body.
document.body.style.display = 'block';
