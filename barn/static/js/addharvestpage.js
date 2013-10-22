//
// addharvestpage
//
// Scripts for the add harvest page.
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',

    ], function ($, Django) {

        $(document).ready(function () {
            $('a.delete').click(function (event) {
                if (!confirm("Are you sure you want to delete this harvest?")) {
                    return false;
                }
            });

            $('#id_gardener_text, #id_variety_text').focusout(function () {
                var gardener = $('#id_gardener_text').val();
                var variety = $('#id_variety_text').val();
                if (gardener && gardener !== '' && variety && variety !== '') {
                    $.getJSON('last_harvest?gardener=' + gardener + '&variety=' + variety, function (h) {
                        $('#id_plants').val(h.plants);
                        $('#id_area').val(h.area);
                    });
                }
            });

        });
    }

);
