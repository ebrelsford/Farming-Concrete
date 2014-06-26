({

    baseUrl: 'js',
    mainConfigFile: 'app.js',
    name: '../bower_components/almond/almond',
    out: 'main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules

        // require()d dependencies
        'bootstrap',
        'addcropcountpage',
        'addgardenspage',
        'addharvestpage',
        'addlookinggoodeventpage',
        'addparticipationhourspage',
        'addsales',
        'chosen.jquery_ready',
        'leaflet.basicmap',
        'landfilldiversionvolumechart',
        'lookinggoodtagset',
        'resig.class',
        'new_widget',
        'newcropwidget',
        'newcropvarietywidget',
        'newgardenerwidget',
        'newprojectwidget',
        'photogallery',
        'recordlistpage',
        'underscore'
    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",

    // We will manually compress JS after
    optimize: "none",

    preserveLicenseComments: true
    
})
