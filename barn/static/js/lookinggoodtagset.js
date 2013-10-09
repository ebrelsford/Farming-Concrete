//
// lookinggoodtagset
//
// Scripts for lookinggood tag set
//

define(
    [
        // Requirements with exports
        'jquery',
        'django-dynamic-formset',
    ], function ($) {

        $(document).ready(function () {
            $('.lookinggood-tag-formset').formset({
                addCssClass: 'add-another-tag btn btn-xs btn-default',
                addText: 'add another comment',
                deleteText: 'delete above comment',
            });
        });

    }

);

