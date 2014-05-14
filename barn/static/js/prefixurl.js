//
// XXX 
// This should be considered a temporary fix until Django.js is fixed to use 
// script prefixes to correct their urls.
// XXX
//
define(['django'], function (Django) {
    return {
        url: function (name, args) {
            var unprefixed = Django.url(name, args);
            if (Django.context.debug !== true) {
                return '/barn' + unprefixed;
            }
            return unprefixed;
        }
    };
});
