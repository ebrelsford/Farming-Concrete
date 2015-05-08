//
// addlookinggoodeventpage
//

var $ = require('jquery');

require('django-dynamic-formset');
require('jquery.expander');

$(document).ready(function () {
    if ($('.add-lookinggood-event-page').length > 0) {
        $('.lookinggood-item-formset').formset({
            addCssClass: 'add-row btn btn-default',
            addText: 'Add another object',
            added: function (row) {
                var gardenPk = $('.lookinggood-item-formset :input[name$=garden]:eq(0)').val();
                row.find(':input[name$=garden]').val(gardenPk);
            },
            prefix: 'lookinggooditem_set'
        });

        $('.photo-formset').formset({
            addCssClass: 'add-row btn btn-default',
            addText: 'Add another photo',
            added: function (row) {
                var gardenPk = $('.photo-formset :input[name$=garden]:eq(0)').val();
                row.find(':input[name$=garden]').val(gardenPk);
            },
            prefix: 'lookinggoodphoto_set'
        });

        $('.list-records .comments').expander({
            slicePoint: 5
        });
    }
});
