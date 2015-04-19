/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

// ES6 polyfill
require("babel/polyfill");

// External libs
const ko = require('knockout');

// Our libs
const LikesPage = require('./likes-page');

class IndexPage extends LikesPage {
}

let index_page = new IndexPage();
ko.applyBindings(index_page);
index_page.init();
