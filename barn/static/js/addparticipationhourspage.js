//
// addparticipationhourspage
//

var $ = require('jquery');
require('django-dynamic-formset');

$(document).ready(function () {
    if ($('.add-participation-hours-page').length > 0) {
        $('.projecthours-formset').formset({
            addCssClass: 'add-row btn btn-default',
            addText: 'Add another participant',
            added: function (row) {
                var gardenPk = $('.projecthours-formset :input[name$=garden]:eq(0)').val();
                row.find(':input[name$=garden]').val(gardenPk);
            },
            prefix: 'projecthours_set'
        });
    }
});
