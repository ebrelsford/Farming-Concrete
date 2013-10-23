requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'bootstrap': '../bower_components/bootstrap/dist/js/bootstrap',
        'colorbox': '../bower_components/colorbox/jquery.colorbox',
        'd3': '../bower_components/d3/d3',
        'django': 'djangojs/django',
        'django-dynamic-formset': '../bower_components/django-dynamic-formset/src/jquery.formset',
        'handlebars': '../bower_components/handlebars.js/dist/handlebars',
        'jquery': '../bower_components/jquery/jquery',
        'jquery.autocomplete': '../bower_components/jquery-autocomplete/jquery.autocomplete',
        'jquery.form': '../bower_components/jquery-form/jquery.form',
        'jquery.spin': '../bower_components/spin.js/jquery.spin',
        'jquery.stupid-table-sort': '../bower_components/stupid-jquery-table-sort/stupidtable',
        'leaflet': '../bower_components/leaflet/leaflet',
        'leaflet.dataoptions': '../bower_components/leaflet.dataoptions/src/leaflet.dataoptions',
        'leaflet.usermarker': '../bower_components/leaflet-usermarker/src/leaflet.usermarker',
        'modernizr': '../bower_components/modernizr/modernizr',
        'pickadate': '../bower_components/pickadate/lib/picker',
        'pickadate.date': '../bower_components/pickadate/lib/picker.date',
        'pickadate.time': '../bower_components/pickadate/lib/picker.time',
        'resig.class': '../bower_components/resig-class/index',
        'select2': '../bower_components/select2/select2',
        'spin': '../bower_components/spin.js/spin',
        'underscore': '../bower_components/underscore/underscore'
    },
    shim: {
        'bootstrap': ['jquery'],
        'chosen.jquery.min': ['jquery'],
        'chosen.jquery_ready': ['jquery', 'chosen.jquery.min'],
        'd3': {
            exports: 'd3'
        },
        'django': {
            deps: ['jquery'],
            exports: 'Django'
        },
        'django-dynamic-formset': ['jquery'],
        'jquery.autocomplete': ['jquery'],
        'jquery.form': ['jquery'],
        'jquery.stupid-table-sort': ['jquery'],
        'handlebars': {
            exports: 'Handlebars'
        },
        'leaflet.usermarker': ['leaflet'],
        'modernizr': {
            exports: 'Modernizr'
        },
        'pickadate': ['jquery'],
        'pickadate.date': ['pickadate'],
        'pickadate.time': ['pickadate'],
        'resig.class': {
            exports: 'Class'
        },
        'select2': ['jquery'],
        'underscore': {
            exports: '_'
        }
    }
});

// Load the main app module to start the app
requirejs(['main']);
