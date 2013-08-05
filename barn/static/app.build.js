({

    baseUrl: 'js',
    //appDir: '.',
    //dir: '../built',

    mainConfigFile: 'app.js',

    name: 'lib/almond',
    out: '../main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules

        // require()d dependencies
        'chosen.jquery_ready',
    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
