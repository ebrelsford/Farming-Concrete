//
// newcropvarietywidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'new_widget',
        'django'

    ], function ($, NewInstanceWidget, Django) {

        var NewCropVarietyWidget = NewInstanceWidget.extend({});

        function loadCropVarieties($crop, $cropVariety) {
            var url = Django.url('crops_variety_list') + '?' + $.param({
                crop: $crop.val()  
            });

            // Disable variety select until we have updated the data
            $cropVariety.select2('enable', false);

            // Select first option
            $cropVariety.select2('val', '');

            // Clear existing options (after the first)
            $cropVariety.find('option:not(:first-of-type)').remove();

            $.getJSON(url, function (data) {
                $.each(data, function (i, variety) {
                    $cropVariety.append(
                        $('<option></option>')
                            .val(variety.pk)
                            .text(variety.name)
                    );
                });
                // Re-enable variety select until we have updated the data
                $cropVariety.select2('enable', true);
            });
        }

        $(document).ready(function () {
            var widget = new NewCropVarietyWidget({
                buttonSelector: '.btn-new-crop-variety',
                selectSelector: 'select[name=crop_variety],select[name$=crop_variety]'
            });

            var cropSelector = 'select[name$=crop]',
                $crop = $(cropSelector),
                cropVarietySelector = widget.options.selectSelector,
                $cropVariety = $(cropVarietySelector);

            // If we are working with formsets, get the variety select
            // that has the same parent as the crop select that changed
            //
            // TODO consider moving into NewInstanceWidget
            if ($('.patch-formset').length > 0) {
                $cropVariety = $crop.nextAll(cropVarietySelector);
            }

            // If something is already selected (eg, on error), load crop
            // varieties as soon as we can
            if ($(cropSelector).val() != '') {
                loadCropVarieties($crop, $cropVariety);
            }

            $(cropSelector).change(function () {
                loadCropVarieties($crop, $cropVariety);
            });

            $(widget.options.buttonSelector).click(function () {
                // Ensure we're getting the right crop select input
                var $cropSelect = $(cropSelector);
                if ($('.patch-formset').length > 0) {
                    $cropSelect = $(this).parents('.patch-formset').find(cropSelector);
                }
                if (!$cropSelect.val()) {
                    alert('Please pick a crop before adding a variety.');
                    return false;
                }
                else {
                    $(widget.options.buttonSelector).removeClass('clicked');
                    $(this).parents('.patch-formset')
                        .find(widget.options.buttonSelector).addClass('clicked');
                }
            });

            var modalSelector = $(widget.options.buttonSelector).data('target');
            $(modalSelector).on('show.bs.modal', function () {
                $.get($(widget.options.buttonSelector).attr('href'), function (content) {
                    var $modalContent = $(modalSelector).find('.modal-content');
                    $modalContent.find('*').remove();
                    $modalContent.append(content);

                    // Find the crop selector relative to the button that was
                    // clicked
                    var crop = $(widget.options.buttonSelector + '.clicked').parents('.patch-formset').find(cropSelector).val();
                    $(modalSelector).find('#id_crop').val(crop);
                });
            });

        });

    }
);
