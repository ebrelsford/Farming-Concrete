//
// Reports
//
// Scripts dealing with the reports section of the Barn.
//

define(['jquery', 'leaflet.basicmap'], function ($) {

    $(document).ready(function () {

        $('.filter').change(function () {
            function buildQueryString() {
                var params = {};
                $('select.filter').each(function () {
                    var selection = $(this).find(':selected').val();
                    if (selection === 'all') {
                        return;
                    }
                    params[$(this).attr('name')] = selection;
                });
                $('.filter[type="checkbox"]:checked').each(function () {
                    params[$(this).attr('name')] = 'yes';
                });
                return params;
            }
            var params = buildQueryString();
            window.location = '/reports/?' + $.param(params);
        });


        // Show info-box

        $('.average-yield').click(function (event) {
            if (!$(this).text()) {
                return;
            }
            var variety = $(this).data('crop-name');
            var year = $(this).data('year');
            $(this).addClass('picked');
            $.get('{% url "estimates_estimatedyield_explain" %}?variety=' + variety + '&year=' + year, function (data) {
                $('body').append($('<div/>')
                    .html(data)
                    .addClass('info-box')
                    .position({
                        my: 'left top',
                        at: 'left top',
                        of: event,
                    })
                );
            });
        });


        // Hide info-box if anything outside of it is clicked

        $(document).click(function (event) {
            if ($(event.target).parents('.info-box').size()) {
                return;
            }
            if ($('.info-box').size()) {
                $('.average-yield').removeClass('picked');
                $('.info-box').remove();
            }
        });
    });

});
