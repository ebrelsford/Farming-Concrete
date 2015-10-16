var browserify = require('browserify'),
    buffer = require('vinyl-buffer'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    jshint = require('gulp-jshint'),
    less = require('gulp-less'),
    minifyCSS = require('gulp-minify-css'),
    path = require('path'),
    plumber = require('gulp-plumber'),
    rename = require('gulp-rename'),
    source = require('vinyl-source-stream'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify'),
    watch = require('gulp-watch'),
    watchify = require('watchify');

var bDev = watchify(browserify({
    debug: true,
    entries: ['./js/main.js'],
    cache: {},
    packageCache: {},
    insertGlobals: true
})).transform({global: true}, 'browserify-shim');

bDev.on('update', makeDevBundle);
bDev.on('log', gutil.log);

var bProd = watchify(browserify({
    entries: ['./js/main.js'],
    insertGlobals: true
})).transform({global: true}, 'browserify-shim');
bProd.on('update', makeProdBundle);
bProd.on('log', gutil.log);

function makeDevBundle() {
    gutil.log('Building dev js');
    return bDev.bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify Error'))
        .pipe(plumber())
        .pipe(source('app.dev.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('dist'));
}

function makeProdBundle() {
    gutil.log('Building prod js');
    return bProd.bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify Error'))
        .pipe(plumber())
        .pipe(source('app.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
}

gulp.task('css-dev', function () {
    return gulp.src('less/**/style.less', { base: 'less' })
        .pipe(plumber())
        .pipe(sourcemaps.init())
            .pipe(less({
                paths: [path.join(__dirname, 'less')]
            }))
        .pipe(sourcemaps.write())
        .pipe(rename('style.dev.css'))
        .pipe(gulp.dest('dist'));
});

gulp.task('css-prod', function () {
    return gulp.src('dist/style.dev.css')
        .pipe(plumber())
        .pipe(minifyCSS())
        .pipe(rename('style.css'))
        .pipe(gulp.dest('dist'));
});

gulp.task('lintjs', function () {
    return gulp.src([
        'gulpfile.js',
        'js/**/*.js',
    ]).pipe(jshint())
    .pipe(jshint.reporter('default'));
});

gulp.task('bundle', function () {
    makeDevBundle();
    makeProdBundle();
});

gulp.task('watch', ['bundle'], function () {
    gulp.watch('less/**/*.less', ['css-dev', 'css-prod']);

    //gulp.watch('js/**/*.js', ['lintjs']);
});
