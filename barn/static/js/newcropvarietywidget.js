//
// newcropvarietywidget
//

var $ = require('jquery');
var Django = require('django');
var NewInstanceWidget = require('./new_widget');

var cropSelector = 'select[name$=crop]',
    formsetSelector = '.patch-formset',
    buttonSelector = '.btn-new-crop-variety',
    selectSelector = 'select[name=crop_variety],select[name$=crop_variety]';

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

//
// Find the crop variety select input relative to an element
//
function findCropVariety($ele, cropVarietySelector) {
    if ($(formsetSelector).length > 0) {
        return $ele.parents(formsetSelector).find(cropVarietySelector);
    }
    return $(cropVarietySelector);
}

//
// Find the crop select input relative to an element
//
function findCrop($ele, cropSelector) {
    if ($(formsetSelector).length > 0) {
        return $ele.parents(formsetSelector).find(cropSelector);
    }
    return $(cropSelector);
}

$(document).ready(function () {
    if ($('.btn-new-crop-variety').length > 0) {
        var widget = new NewCropVarietyWidget({
            buttonSelector: buttonSelector,
            selectSelector: selectSelector
        });

        var cropVarietySelector = widget.options.selectSelector;
        var $crops = $(cropSelector);

        // If something is already selected (eg, on error), load crop
        // varieties as soon as we can
        $crops.each(function () {
            if ($(this).val() !== '') {
                loadCropVarieties($(this),
                                  findCropVariety($(this), cropVarietySelector));
            }
        });

        // Update variety selector when crops input change
        $crops.change(function () {
            loadCropVarieties($(this), findCropVariety($(this), cropVarietySelector));
        });

        $(widget.options.buttonSelector).click(function () {
            // Ensure a crop is selected
            var $crop = findCrop($(this), cropSelector);
            if (!$crop.val()) {
                alert('Please pick a crop before adding a variety.');
                return false;
            }
            $(widget.options.buttonSelector).removeClass('clicked');
            $(this).addClass('clicked');
        });

        var modalSelector = $(widget.options.buttonSelector).data('target');
        $(modalSelector).on('show.bs.modal', function (e) {
            $.get($(e.relatedTarget).attr('href'), function (content) {
                // Create modal
                var $modalContent = $(modalSelector).find('.modal-content');
                $modalContent.find('*').remove();
                $modalContent.append(content);

                // Grab crop value from crop select input
                var crop = findCrop($(e.relatedTarget), cropSelector).val();
                $(modalSelector).find('#id_crop').val(crop);

                // Focus on variety name field
                $('.modal:visible form :input:visible:eq(0)').focus();
            });
        });

    }
});
