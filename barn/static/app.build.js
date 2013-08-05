({

    baseUrl: 'js',
    mainConfigFile: 'app.js',
    name: '../lib/almond',
    out: 'main-built.js',
    include: [

        // Main module
        'main',

        // Per-page modules

        // require()d dependencies
        '../lib/bootstrap/bootstrap',

    ],
    insertRequire: ['main'],

    // Let django-compressor take care of CSS
    optimizeCss: "none",
    optimize: "uglify2",

    preserveLicenseComments: true,
    
})
