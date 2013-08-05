//
// main.js
//
// Scripts that should run on every page.
//

define(
    [
        'jquery',
    ], function ($) {

        /*
        * Global form-related scripts
        */
        $(document).ready(function () {

            /*
             * Always give focus to the first visible input.
             */
            if ($('input:visible').length > 0) {
                $('input:visible:first').focus();
            }

            /*
             * Disable submit buttons on forms once they have been submitted once.
             */
            $('form').submit(function () {
                $(this).find('input[type="submit"]').attr('disabled', 'disabled');
            });

        });


        /*
        * Page-specific modules
        */
        // Load page-specific modules, eg:
        /*
        if ($('.lot-base-page').length > 0) {
            require(['lotbasepage']);
        }
        */

});
