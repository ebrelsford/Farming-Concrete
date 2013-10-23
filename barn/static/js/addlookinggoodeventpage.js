//
// addlookinggoodeventpage
//

define(
    [
        // Requirements with exports
        'jquery',

        'django-dynamic-formset',

    ], function ($) {

        $(document).ready(function () {
            $('.photo-formset').formset({
                addCssClass: 'add-row col-lg-6 col-lg-offset-4',
                addText: 'Add another photo',
                added: function (row) {
                    var gardenPk = $('.photo-formset :input[name$=garden]:eq(0)').val();
                    row.find(':input[name$=garden]').val(gardenPk);
                },
                prefix: 'lookinggoodphoto_set'
            });
        });

    }
);
