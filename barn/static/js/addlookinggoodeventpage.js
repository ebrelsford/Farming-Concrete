//
// addlookinggoodeventpage
//

define(
    [
        // Requirements with exports
        'jquery',

        'django-dynamic-formset',
        'jquery.expander'

    ], function ($) {

        $(document).ready(function () {

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

        });

    }
);
