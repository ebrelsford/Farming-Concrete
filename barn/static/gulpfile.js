var gulp = require('gulp'),
    less = require('gulp-less'),
    minifyCSS = require('gulp-minify-css'),
    path = require('path'),
    sourcemaps = require('gulp-sourcemaps'),
    watch = require('gulp-watch');

gulp.task('watch', function () {

    // Watch LESS files for development
    watch('css/**/*.less', function () {
        return gulp.src('css/**/style.less', { base: 'css' })
            .pipe(sourcemaps.init())
                .pipe(less({
                    paths: [path.join(__dirname, 'css')]
                }))
            .pipe(sourcemaps.write())
            .pipe(gulp.dest('css'));
    });

    // Watch style.css for production
    watch('css/style.css', function () {
        return gulp.src('css/style.css')
            .pipe(minifyCSS())
            .pipe(gulp.dest('dist'));
    });
});
