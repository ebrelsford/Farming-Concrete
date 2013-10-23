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
                addCssClass: 'add-row col-lg-6 col-lg-offset-4',
                addText: 'Add another participant',
            });
        });

    }
);
