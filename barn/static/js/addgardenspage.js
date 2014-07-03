//
// addgardenspage
//
// Scripts for the add gardens page.
//

define(
    [
        // Requirements with exports
        'jquery',
        'prefixurl',
        'leaflet',
        'geocode',

        // Other requirements
        'jquery.spin',
        'leaflet.dataoptions',
        'leaflet.usermarker'
    ], function ($, prefixurl, L, geocode) {

        var map;

        function updateSuggestions() {
            var baseUrl = prefixurl.url('farmingconcrete_gardens_suggest'),
                name = $('#id_name').val(),
                $wrapper = $('.garden-suggestions-wrapper');
            $wrapper
                .spin('large')
                .addClass('is-loading')
                .load(baseUrl + '?' + $.param({ name: name }), function () {
                    $wrapper
                        .spin(false)
                        .removeClass('is-loading');
                    activateSuggestedGardens();
                });
        }

        function clearSuggestions() {
            $('.garden-suggestions-wrapper').empty();
        }

        function activateSuggestedGardens() {
            $('.garden-suggestion').click(function () {
                selectSuggestedGarden($(this).data('pk'));
            });
        }

        function initializeMap() {
            var map = L.map('add-garden-map');
            L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                mapboxId: map.options.mapboxId
            }).addTo(map);
            return map;
        }

        function selectSuggestedGarden(pk) {
            window.location.href = prefixurl.url('farmingconcrete_gardens_suggest_add', { 'pk': pk });
        }

        function geocodeAddress() {
            var address = $('#id_address').val(),
                city = $('#id_city').val(),
                state = $('#id_state').val(),
                formattedAddress = address + ', ' + city + ', ' + state;

            geocode.geocode(formattedAddress, state, function (result, status) {
                if (status === 'OK' && result) {
                    showGeocodedResultOnMap(result);
                    setGardenLocation(result);
                }
            });
        }

        function roundCoordinate(c) {
            return Math.round(c * 10000) / 10000;
        }

        function setGardenLocation(result) {
            var lat = geocode.get_latitude(result),
                lng = geocode.get_longitude(result);
            $('#id_latitude').val(roundCoordinate(lat));
            $('#id_longitude').val(roundCoordinate(lng));
            $('#id_address').val(geocode.get_street(result));
            $('#id_neighborhood').val(geocode.get_neighborhood(result));
            $('#id_city').val(geocode.get_city(result));
            $('#id_state').val(geocode.get_state(result));
            $('#id_zip').val(geocode.get_zip(result));

            var borough = geocode.get_borough(result),
                $boroughOption = $('#id_borough option[value="' + borough + '"]');
            if ($boroughOption.length > 0) {
                $boroughOption
                    .prop('selected', true)
                    .parents('.form-group').show();
            }
        }

        function showPointOnMap(lat, lng) {
            var latlng = [lat, lng],
                marker = L.userMarker(latlng, { smallIcon: true }).addTo(map);
            map.setView(latlng, 15);
        }

        function showGeocodedResultOnMap(result) {
            showPointOnMap(geocode.get_latitude(result),
                           geocode.get_longitude(result));
        }

        $(document).ready(function () {
            map = initializeMap();

            var lat = $('#id_latitude').val(),
                lng = $('#id_longitude').val();
            if (lat && lng) {
                showPointOnMap(lat, lng);
            }

            // If creating a new garden, enable suggestions
            if ($('#id_name').val() === '') {
                $('#id_name').keyup(function () {
                    if ($(this).val().length >= 5) {
                        updateSuggestions();
                    }
                    else {
                        clearSuggestions();
                    }
                });
            }

            $('#id_address,#id_city,#id_state').change(geocodeAddress);

        });

    }

);
