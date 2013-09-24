requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'bootstrap': '../bower_components/bootstrap/dist/js/bootstrap',
        'django': 'djangojs/django',
        'handlebars': '../bower_components/handlebars.js/dist/handlebars',
        'jquery': '../bower_components/jquery/jquery',
        'jquery.form': '../bower_components/jquery-form/jquery.form',
        'jquery.spin': '../bower_components/spin.js/jquery.spin',
        'leaflet': '../bower_components/leaflet/leaflet',
        'leaflet.usermarker': '../bower_components/leaflet-usermarker/src/leaflet.usermarker',
        'modernizr': '../bower_components/modernizr/modernizr',
        'spin': '../bower_components/spin.js/spin',
        'underscore': '../bower_components/underscore/underscore',
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
