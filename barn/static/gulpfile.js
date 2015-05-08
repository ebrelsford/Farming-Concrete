var browserify = require('browserify'),
    buffer = require('vinyl-buffer'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    less = require('gulp-less'),
    minifyCSS = require('gulp-minify-css'),
    path = require('path'),
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
        .pipe(source('app.dev.js'))
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
        .pipe(source('app.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
}

gulp.task('watch', function () {

    // Watch LESS files for development
    watch('css/**/*.less', function () {
        return gulp.src('css/**/style.less', { base: 'css' })
            .pipe(sourcemaps.init())
                .pipe(less({
                    paths: [path.join(__dirname, 'css')]
                }))
            .pipe(sourcemaps.write())
            .pipe(rename('style.dev.css'))
            .pipe(gulp.dest('dist'));
    });

    // Watch style.css for production
    watch('css/style.css', function () {
        return gulp.src('css/style.css')
            .pipe(minifyCSS())
            .pipe(gulp.dest('dist'));
    });

    // Watch JS for development
    watch('js/**/*.js', makeDevBundle);

    watch('dist/app.dev.js', makeProdBundle);
});
