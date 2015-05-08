//
// addharvestpage
//
// Scripts for the add harvest page.
//

var $ = require('jquery');
var Django = require('django');

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
    }
});
