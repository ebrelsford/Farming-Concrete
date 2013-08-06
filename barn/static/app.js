requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'bootstrap': '../lib/bootstrap/js/bootstrap',
        'django': 'djangojs/django',
        'jquery': '../lib/jquery-1.10.2.min',
        'jquery.spin': '../lib/jquery.spin',
        'jqueryui': 'lib/jquery-ui-1.10.3.custom',
        'leaflet': '../lib/leaflet/leaflet-src',
        'leaflet.usermarker': '../lib/leaflet-usermarker/leaflet.usermarker',
        'spin': '../lib/spin',
        'underscore': 'lib/underscore-min',
    },
    shim: {
        'bootstrap': ['jquery'],
        'django': {
            'deps': ['jquery'],
            'exports': 'Django',
        },
        'leaflet.usermarker': ['leaflet'],
        'underscore': {
            exports: '_',
        },
    },
});

// Load the main app module to start the app
requirejs(['main']);
