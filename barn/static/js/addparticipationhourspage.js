//
// addparticipationhourspage
//

define(
    [
        // Requirements with exports
        'jquery',

        'django-dynamic-formset',

    ], function ($) {

        $(document).ready(function () {
            $('.projecthours-formset').formset({
                addCssClass: 'add-row btn btn-default',
                addText: 'Add another participant',
                added: function (row) {
                    var gardenPk = $('.projecthours-formset :input[name$=garden]:eq(0)').val();
                    row.find(':input[name$=garden]').val(gardenPk);
                },
                prefix: 'projecthours_set'
            });
        });

    }
);
