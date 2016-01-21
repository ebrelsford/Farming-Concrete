//
// addharvestpage
//
// Scripts for the add harvest page.
//

var $ = require('jquery'),
    Django = require('django'),
    _ = require('underscore'),
    queryString = require('query-string');

$(document).ready(function () {
    if ($('.add-harvest-page').length > 0) {
        $('a.delete').click(function (event) {
            if (!confirm("Are you sure you want to delete this harvest?")) {
                return false;
            }
        });

        $('#id_gardener, #id_crop').change(function () {
            var gardener = $('#id_gardener').val();
            var crop = $('#id_crop').val();
            if (gardener && gardener !== '' && crop && crop !== '') {
                var params = {
                    gardener: gardener,
                    crop: crop
                };
                $.getJSON('last_harvest?' + $.param(params), function (h) {
                    $('#id_plants').val(h.plants);
                    $('#id_area').val(h.area);
                });
            }
        });

        var measurementSystem = $('.metric-add-record').data('measurement-system'),
            params = queryString.parse(location.search),
            unitPicker = $(':input[name=weight_1]'),
            validUnits = $(':input[name=weight_1] option').map(function () {
                return $(this).attr('value');
            }).get();

        if (params.units && _.contains(validUnits, params.units)) {
            unitPicker.val(params.units);
        }
        else {
            if (measurementSystem === 'metric') {
                unitPicker.val('kg');
            }
            else if (measurementSystem === 'imperial') {
                unitPicker.val('lb');
            }
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
