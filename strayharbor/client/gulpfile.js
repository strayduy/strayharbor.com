/* jshint node: true */
'use strict';

var babelify            = require('babelify');
var browser_sync        = require('browser-sync');
var browserify          = require('browserify');
var concat              = require('gulp-concat');
var concat_css          = require('gulp-concat-css');
var gulp                = require('gulp');
var gutil               = require('gulp-util');
var minify_css          = require('gulp-minify-css');
var rename              = require('gulp-rename');
var streamify           = require('gulp-streamify');
var stringify           = require('stringify');
var uglify              = require('gulp-uglify');
var vinyl_source_stream = require('vinyl-source-stream');
var watchify            = require('watchify');

gulp.task('default', ['build-all']);
gulp.task('build-all', ['vendor', 'index']);
gulp.task('vendor', ['vendor-js', 'vendor-css', 'vendor-fonts']);
gulp.task('index', ['index-js', 'index-css']);

gulp.task('browser-sync', function() {
    browser_sync({
        proxy: 'localhost:5000',
        ui: false,
    });
});

gulp.task('vendor-js', function() {
    var vendor_js = [
        './bower_components/jquery/dist/jquery.js',
        './bower_components/bootstrap/dist/js/bootstrap.js',
        './bower_components/lodash/lodash.js',
        './bower_components/knockout/dist/knockout.debug.js'
    ];
    var DEST = './static/vendor/js';

    return gulp.src(vendor_js)
        .pipe(concat('vendor.js'))
        .pipe(gulp.dest(DEST))
        .pipe(uglify())
        .pipe(rename({extname: '.min.js'}))
        .pipe(gulp.dest(DEST));
});

gulp.task('vendor-css', function() {
    var vendor_css = [
        './bower_components/bootstrap/dist/css/bootstrap.css',
        './bower_components/font-awesome/css/font-awesome.css'
    ];
    var DEST = './static/vendor/css';

    return gulp.src(vendor_css)
        .pipe(concat_css('vendor.css', {rebaseUrls: false}))
        .pipe(gulp.dest(DEST))
        .pipe(minify_css({rebase: false}))
        .pipe(rename({extname: '.min.css'}))
        .pipe(gulp.dest(DEST));
});

gulp.task('vendor-fonts', function() {
    var vendor_fonts = [
        './bower_components/bootstrap/dist/fonts/*',
        './bower_components/font-awesome/fonts/*'
    ];
    var DEST = './static/vendor/fonts';

    return gulp.src(vendor_fonts)
        .pipe(gulp.dest(DEST));
});

gulp.task('index-js', function() {
    return bundle_index(false);
});

gulp.task('index-css', function() {
    var index_css = [
        './src/**/*.css',
    ];
    var DEST = './static/app/css';

    return gulp.src(index_css)
        .pipe(concat_css('index.css'))
        .pipe(gulp.dest(DEST))
        .pipe(minify_css())
        .pipe(rename({extname: '.min.css'}))
        .pipe(gulp.dest(DEST));
});

gulp.task('watch-index', ['browser-sync'], function() {
    gulp.watch(['./src/**/*.css'], ['index-css', browser_sync.reload]);
    gulp.watch(['../templates/*.html'], [browser_sync.reload]);
    bundle_index(true);
});

function bundle_index(watch) {
    var bundler = browserify('./src/index.js');
    var DEST = './static/app/js';

    function bundle() {
        return bundler
            .transform(babelify)
            .bundle()
            .pipe(vinyl_source_stream('index.bundle.js'))
            .pipe(gulp.dest(DEST))
            .pipe(streamify(uglify()))
            .pipe(rename({extname: '.min.js'}))
            .pipe(gulp.dest(DEST))
            .pipe(browser_sync.reload({stream: true}));
    }

    if (watch) {
        bundler = watchify(bundler);
        bundler.transform(stringify(['.html']));
        bundler.on('update', bundle);
        bundler.on('log', gutil.log);
    }
    else {
        bundler.transform(stringify(['.html']));
    }

    return bundle();
}
