requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'bootstrap': '../lib/bootstrap/js/bootstrap',
        'django': 'djangojs/django',
        'jquery': '../lib/jquery-1.10.2.min',
        'jqueryui': 'lib/jquery-ui-1.10.3.custom',
        'underscore': 'lib/underscore-min',
        'spin': 'lib/spin.min',
    },
    shim: {
        'bootstrap': ['jquery'],
        'django': {
            'deps': ['jquery'],
            'exports': 'Django',
        },
        'underscore': {
            exports: '_',
        },
    },
});

// Load the main app module to start the app
requirejs(['main']);
