//
// addcompostweight
//
// Update weight units picker based on the garden's preferred measurement
// system.
//

var $ = require('jquery');

$(document).ready(function () {
    if ($('.add-compost-weight').length > 0) {
        var measurementSystem = $('.metric-add-record').data('measurement-system'),
            unitPicker = $(':input[name=weight_1]');
        if (measurementSystem === 'metric') {
            unitPicker.val('kg');
        }
        else if (measurementSystem === 'imperial') {
            unitPicker.val('lb');
        }

        var $helpButton = $('<span></span>')
            .addClass('help_link')
            .text('?')
            .tooltip({
                title: 'Default units can be changed by editing your garden. This setting also determines the units you will see when downloading data and reports.'
            });
        $('.field-weight .control-label:eq(0)').append($helpButton);

    }
});
