var gulp = require('gulp');
var browserify = require('browserify');
var reactify = require('reactify');
var source = require('vinyl-source-stream');

gulp.task('browserify', function() {
	browserify('./src/client/js/main.js')
		.transform('reactify')
		.bundle()
		.pipe(source('main.js'))
		.pipe(gulp.dest('src/server/static'));
});

gulp.task('copy', function() {
	gulp.src('src/client/app.html')
		.pipe(gulp.dest('src/server/pkg/views'));

	gulp.src('src/client/assets/**/*.*')
		.pipe(gulp.dest('src/server/static'));
});

gulp.task('default', ['browserify', 'copy'], function() {
	return gulp.watch('src/client/**/*.*', ['browserify', 'copy'])
});
