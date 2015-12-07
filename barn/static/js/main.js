//
// main.js
//
// Scripts that should run on every page.
//

var $ = require('jquery');

require('browsernizr/lib/mq');
require('browsernizr/test/input');
require('browsernizr/test/inputtypes');
var Modernizr = require('browsernizr');

var rome = require('rome');

require('bootstrap');
require('jquery-autocomplete');
require('jquery-stupid-table-sort');

require('./farmingconcrete');
require('./feedback');
require('./listrecords');


/*
* Global form-related scripts
*/
$(document).ready(function () {

    /*
     * Always give focus to the first visible input.
     */
    $(':input:visible:first:not([type="date"])').focus();

    /*
     * Disable submit buttons on forms once they have been submitted once.
     */
    $('form').submit(function () {
        $(this).find('input[type="submit"]').attr('disabled', 'disabled');
    });

    /*
     * Add rome if no native datepicker available or we're likely
     * on a desktop browser.
     */
    if (!Modernizr.inputtypes.date || Modernizr.mq('(min-width: 799px)')) {
        $('input[type=date]').each(function () {
            rome($(this)[0], {
                max: $(this).attr('max'),
                time: false
            });
        });
        $('.recorded-input-addon').click(function () {
            rome.find($(this).prevAll('input')[0]).show();
            return false;
        });
    }

    /*
     * Hide help text if it's in form fields' placeholder attributes.
     */
    if (Modernizr.input.placeholder) {
        $(':input[type="text"] ~ .help-text, textarea ~ .help-text').hide();
    }

    /*
     * Add pickadate if time inputs
     */
    if (!Modernizr.inputtypes.time) {
        $('input[type=time]').each(function () {
            rome($(this)[0], {
                max: $(this).attr('max'),
                time: true
            });
        });
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
 * Widgets
 */
require('./leaflet.basicmap');
require('./newcropwidget');
require('./newcropvarietywidget');
require('./newgardenerwidget');
require('./newprojectwidget');
require('./photogallery');

/*
 * Page-specific modules
 */
require('./addcompostweight');
require('./addcropcountpage');
require('./addgardenspage');
require('./addharvestpage');
require('./addlookinggoodeventpage');
require('./addparticipationhourspage');
require('./addsales');
require('./addgardengroupadmin');
require('./gardendetailpage');
require('./gardengroupmemberlist');
require('./gardenmemberlist');
require('./index');
require('./listrecords');
require('./recordlistpage');
require('./reports');
require('./landfilldiversionvolumechart');
