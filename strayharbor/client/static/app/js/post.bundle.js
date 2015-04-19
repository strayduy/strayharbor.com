(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

var _classCallCheck = function (instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } };

var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

// External libs
var $ = (window.$);
var ko = (window.ko);

// Components
require('./components/post-entry');

var PostPage = (function () {
    function PostPage(params) {
        _classCallCheck(this, PostPage);

        this.post = ko.observable();
        this.is_loaded = ko.observable(false);
    }

    _createClass(PostPage, [{
        key: 'init',
        value: function init() {
            var _this = this;

            $.get(window.location.pathname + '.json').done(function (response) {
                _this.post(response.post);
                _this.is_loaded(true);
            });
        }
    }]);

    return PostPage;
})();

var post_page = new PostPage();
ko.applyBindings(post_page);
post_page.init();

},{"./components/post-entry":2}],2:[function(require,module,exports){
/* jshint browserify: true */
/* jshint esnext: true */
'use strict';

var _classCallCheck = function (instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } };

// External libs
var ko = (window.ko);

// Component template
var template = require('./post-entry.html');

var PostEntry = function PostEntry(params) {
    _classCallCheck(this, PostEntry);

    this.post = params.post;
};

ko.components.register('post-entry', {
    viewModel: PostEntry,
    template: template });

},{"./post-entry.html":3}],3:[function(require,module,exports){
module.exports = "<div class=\"post-entry panel panel-default\">\n    <div class=\"panel-body\">\n        <h3 class=\"post-title\">\n            <a data-bind=\"html: ko.unwrap(post).title, attr: {href: ko.unwrap(post).url}\"></a>\n        </h3>\n        <div class=\"post-content\" data-bind=\"html: ko.unwrap(post).content\">\n        </div>\n        <div class=\"text-right\">\n            <a class=\"posts-link\" href=\"/posts/\">\n                self.posts\n            </a>\n        </div>\n    </div>\n</div>\n";

},{}]},{},[1]);
