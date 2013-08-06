//
// addgardenspage
//
// Scripts for the add gardens page.
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',
        'leaflet',
        'geocode',

        // Other requirements
        'jquery.spin',
        'leaflet.usermarker'
    ], function ($, Django, L, geocode) {

        var map;

        function updateSuggestions() {
            var baseUrl = Django.url('farmingconcrete_gardens_suggest'),
                name = $('#id_name').val(),
                url = baseUrl + '?name=' + name,
                $wrapper = $('.garden-suggestions-wrapper');
            $wrapper
                .spin('large')
                .addClass('is-loading')
                .load(url, function () {
                    $wrapper
                        .spin(false)
                        .removeClass('is-loading');
                    activateSuggestedGardens();
                });
        }

        function activateSuggestedGardens() {
            $('.garden-suggestion').click(function () {
                selectSuggestedGarden($(this).data('pk'));
            });
        }

        function initializeMap() {
            var map = L.map('add-garden-map', {
                center: [40.71, -73.98],
                zoom: 8
            });
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: '781b27aa166a49e1a398cd9b38a81cdf',
                styleId: '24559'
            }).addTo(map);
            return map;
        }

        function selectSuggestedGarden(pk) {
            window.location.href = Django.url('farmingconcrete_gardens_suggest_add', { 'pk': pk });
        }

        function geocodeAddress() {
            var address = $('#id_address').val(),
                city = $('#id_city').val(),
                state = $('#id_state').val(),
                formattedAddress = address + ', ' + city + ', ' + state;

            geocode(formattedAddress, state, function (result, status) {
                if (status === 'OK' && result) {
                    showGardenOnMap(result);
                }
            });
        }

        function showGardenOnMap(result) {
            var latlng = [result.geometry.location.lb, result.geometry.location.mb],
                marker = L.userMarker(latlng, { smallIcon: true }).addTo(map);
            map.setView(latlng, 15);
        }

        $(document).ready(function () {
            map = initializeMap();

            $('#id_name').keyup(function () {
                if ($(this).val().length >= 5) {
                    updateSuggestions();
                }
            });

            $('#id_address,#id_city,#id_state').change(geocodeAddress);

        });

    }

);
