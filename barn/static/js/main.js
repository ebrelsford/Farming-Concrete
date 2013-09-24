//
// main.js
//
// Scripts that should run on every page.
//

define(
    [
        'jquery',
        'modernizr',

        'bootstrap',
        'feedback',
    ], function ($, Modernizr) {

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

            /*
             * Add jQuery-ui datepicker if no native datepicker available
             */
            if (!Modernizr.inputtypes.date) {
                $('input[type=date]').datepicker();
            }

        });


        /*
         * Page-specific modules
         */

        if ($('.add-gardens-page').length > 0) {
            require(['addgardenspage']);
        }

        if ($('.main-index-page').length > 0) {
            require(['leaflet.basicmap']);
        }

        if ($('.map-base-page').length > 0) {
            require(['leaflet.basicmap']);
        }

        if ($('.btn-participation-new-project').length > 0) {
            require(['newprojectwidget']);
        }

        if ($('.btn-harvestcount-new-gardener').length > 0) {
            require(['newgardenerwidget']);
        }

    }
);
