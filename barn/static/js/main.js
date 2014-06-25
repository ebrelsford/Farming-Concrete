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
        'listrecords',
        'pickadate.date',
        'pickadate.time',
        'select2'
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
                $('.recorded-input-addon').click(function () {
                    $(this).prevAll('input').pickadate('open');
                    return false;
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

            /*
             * Add tooltips where necessary
             */
            $('.tooltip-trigger').tooltip();

            /*
             * Add select2 support
             */
            $('.select2-basic-select').select2();

        });


        /*
         * Page-specific modules
         */

        if ($('.add-cropcount-page').length > 0) {
            require(['addcropcountpage']);
        }

        if ($('.add-gardens-page').length > 0) {
            require(['addgardenspage']);
        }

        if ($('.add-harvest-page').length > 0) {
            require(['addharvestpage']);
        }

        if ($('.add-lookinggood-event-page').length > 0) {
            require(['addlookinggoodeventpage']);
        }

        if ($('.add-participation-hours-page').length > 0) {
            require(['addparticipationhourspage']);
        }

        if ($('.record-list-page').length > 0) {
            require(['listrecords']);
        }

        if ($('.main-index-page').length > 0) {
            require(['leaflet.basicmap']);
        }

        if ($('.map-base-page').length > 0) {
            require(['leaflet.basicmap']);
        }

        if ($('.photo-gallery').length > 0) {
            require(['photogallery']);
        }

        if ($('.btn-new-project').length > 0) {
            require(['newprojectwidget']);
        }

        if ($('.btn-new-crop').length > 0) {
            require(['newcropwidget']);
        }

        if ($('.btn-new-crop-variety').length > 0) {
            require(['newcropvarietywidget']);
        }

        if ($('.btn-new-gardener').length > 0) {
            require(['newgardenerwidget']);
        }

        if ($('.record-list-page').length > 0) {
            require(['recordlistpage']);
        }

        if ($('.reports-page').length > 0) {
            require(['reports']);
        }

        if ($('.landfilldiversion-volume-chart').length > 0) {
            require(['landfilldiversionvolumechart']);
        }

    }
);
