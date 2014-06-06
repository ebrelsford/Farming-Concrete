//
// addcropcountpage
//

define(
    [
        // Requirements with exports
        'jquery',

        'django-dynamic-formset',
        'jquery.expander'

    ], function ($) {

        $(document).ready(function () {
            // Copy added_by and garden from bed form
            $('.patch-formset :input[name$=added_by]').val($(':input#id_added_by').val());
            $('.patch-formset :input[name$=garden]').val($(':input#id_garden').val());

            // Create a version of the formset without select2 enabled
            $('.select2-basic-select').select2('destroy');
            $('.patch-formset:eq(0)').clone().attr('id', 'form-template').appendTo('body').hide();
            $('.patch-formset:visible .select2-basic-select').select2();

            // Every patch gets the same recorded date on load, then when it 
            // changes
            $('.patch-formset :input[name$=recorded]').val($('#id_recorded').val());
            $('#id_recorded').change(function () {
                $('.patch-formset :input[name$=recorded]').val($(this).val());
            });

            $('.patch-formset:visible').formset({
                addCssClass: 'add-row btn btn-default',
                addText: 'Add another crop',
                added: function (row) {
                    // Manually enable select2 each time a new row is added
                    row.find('.select2-basic-select').select2();
                    var gardenPk = $('.patch-formset :input[name$=garden]:eq(0)').val();
                    row.find(':input[name$=garden]').val(gardenPk);
                    var addedBy = $('.patch-formset :input[name$=added_by]:eq(0)').val();
                    row.find(':input[name$=added_by]').val(addedBy);
                },
                formTemplate: $('#form-template'),
                prefix: 'patch_set'
            });

        });

    }
);
