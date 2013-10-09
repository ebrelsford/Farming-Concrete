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
        'farmingconcrete',
        'feedback',
        'jquery.autocomplete',
        'jquery.stupid-table-sort',
        'pickadate.date',
        'pickadate.time'
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
             * Add pickadate if no native datepicker available
             */
            if (!Modernizr.inputtypes.date) {
                $('input[type=date]').each(function () {
                    var max = $(this).attr('max');
                    $(this).pickadate({
                        format: 'mm/dd/yyyy',
                        'max': max
                    });
                });
            }

            /*
             * Add pickadate if time inputs
             */
            if (!Modernizr.inputtypes.time) {
                $('input[type=time]').pickatime();
            }

            /*
             * Always add sorting to sorted tables
             */
            $('table.sorted').stupidtable();

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

        if ($('.reports-page').length > 0) {
            require(['reports']);
        }

        if ($('.lookinggood-tag-formset').length > 0) {
            require(['lookinggoodtagset']);
        }

    }
);
