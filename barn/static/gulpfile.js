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

var bDev = watchify(browserify('./js/main.js', {
    debug: true,
    insertGlobals: true
})); 
bDev.on('update', makeDevBundle);
bDev.on('log', gutil.log);

var bProd = watchify(browserify('./js/main.js', { insertGlobals: true })); 
bProd.on('update', makeProdBundle);
bProd.on('log', gutil.log);

function makeDevBundle() {
    gutil.log('Building dev js');
    return bDev
        .transform({global: true}, 'browserify-shim')
        .bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify Error'))
        .pipe(plumber())
        .pipe(source('app.dev.js'))
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(buffer())
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('dist'));
}

function makeProdBundle() {
    gutil.log('Building prod js');
    return bProd
        .transform({global: true}, 'browserify-shim')
        .bundle()
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
    return gulp.src('dist/style.css')
        .pipe(plumber())
        .pipe(minifyCSS())
        .pipe(gulp.dest('dist'));
});

gulp.task('lintjs', function () {
    return gulp.src([
        'gulpfile.js',
        'js/**/*.js',
    ]).pipe(jshint())
    .pipe(jshint.reporter('default'));
});

gulp.task('watch', function () {
    gulp.watch('less/**/*.less', ['css-dev', 'css-prod']);

    gulp.watch('js/**/*.js', ['lintjs']);

    // Watch JS for development
    watch('js/**/*.js', makeDevBundle);

    watch('dist/app.dev.js', makeProdBundle);
});
