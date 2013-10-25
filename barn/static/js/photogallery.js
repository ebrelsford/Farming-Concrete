//
// photogallery
//

define(
    [
        // Requirements with exports
        'jquery',

        'colorbox',

    ], function ($) {

        $(document).ready(function () {

            $('.photo-gallery a').colorbox({
                rel: 'gal',
            });

        });

    }
);
