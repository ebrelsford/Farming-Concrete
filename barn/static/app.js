requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'jquery': '../lib/jquery-1.10.2.min',
        'jqueryui': 'lib/jquery-ui-1.10.3.custom',
        'leaflet': 'lib/leaflet',
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
        'Control.Loading': ['leaflet'],
        'Leaflet.Bing': ['leaflet'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
    },
});

// Load the main app module to start the app
requirejs(['main']);
