requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'bootstrap': '../lib/bootstrap/js/bootstrap',
        'django': 'djangojs/django',
        'handlebars': '../lib/handlebars',
        'jquery': '../lib/jquery-1.10.2.min',
        'jquery.form': '../lib/jquery.form',
        'jquery.spin': '../lib/jquery.spin',
        'jqueryui': '../lib/jquery-ui/js/jquery-ui-1.10.3.custom',
        'leaflet': '../lib/leaflet/leaflet-src',
        'leaflet.usermarker': '../lib/leaflet-usermarker/leaflet.usermarker',
        'modernizr': '../lib/modernizr',
        'spin': '../lib/spin',
        'underscore': '../lib/underscore-min',
    },
    shim: {
        'bootstrap': ['jquery'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
        'django': {
            deps: ['jquery'],
            exports: 'Django',
        },
        'jquery.form': ['jquery'],
        'jqueryui': ['jquery'],
        'handlebars': {
            exports: 'Handlebars',
        },
        'leaflet.usermarker': ['leaflet'],
        'modernizr': {
            exports: 'Modernizr',
        },
        'underscore': {
            exports: '_',
        },
    },
});

// Load the main app module to start the app
requirejs(['main']);
