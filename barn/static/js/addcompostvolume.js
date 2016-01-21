//
// addcompostvolume
//
// Update volume units picker based on the garden's preferred measurement
// system.
//

var $ = require('jquery'),
    _ = require('underscore'),
    queryString = require('query-string');

$(document).ready(function () {
    if ($('.add-compost-volume').length > 0) {
        var measurementSystem = $('.metric-add-record').data('measurement-system'),
            params = queryString.parse(location.search),
            unitPicker = $(':input[name=volume_1]'),
            validUnits = $(':input[name=volume_1] option').map(function () {
                return $(this).attr('value');
            }).get();

        if (params.units && _.contains(validUnits, params.units)) {
            unitPicker.val(params.units);
        }
        else {
            if (measurementSystem === 'metric') {
                unitPicker.val('l');
            }
            else if (measurementSystem === 'imperial') {
                unitPicker.val('us_g');
            }
        }

        var $helpButton = $('<span></span>')
            .addClass('help_link')
            .text('?')
            .tooltip({
                title: 'Default units can be changed by editing your garden. This setting also determines the units you will see when downloading data and reports.'
            });
        $('.field-volume .control-label:eq(0)').append($helpButton);

    }
});
