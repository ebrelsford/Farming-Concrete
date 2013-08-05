requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'jquery': '../lib/jquery-1.10.2.min',
        'jqueryui': 'lib/jquery-ui-1.10.3.custom',
        'underscore': 'lib/underscore-min',
        'spin': 'lib/spin.min',
    },
    shim: {
        'underscore': {
            exports: '_',
        },
        'bootstrap': {
            deps: ['jquery'],
        },
    },
});

// Load the main app module to start the app
requirejs(['main']);
