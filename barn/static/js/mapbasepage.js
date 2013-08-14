//
// mapbasepage
//
// Map base page module.
//

define(
    [
        // Requirements with exports
        'jquery',
        'leaflet',
        'django',
        'handlebars',
        'underscore',

        // Requirements without exports
        'leaflet.dataconfig'

    ], function ($, L, Django, Handlebars, _) {
        var mapParams = ['cropcount', 'gardentype', 'year'];

        function initializeMap() {
            var map = L.map('map');
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
            return map;
        }

        function addOverlay(map) {
            var url = Django.url('farmingconcrete_gardens_geojson');
            url += '?' + $.param(_.pick(map.options, mapParams));

            var popupTemplate = Handlebars.compile($('#popup-template').html());

            $.getJSON(url, function (data) {
                var gardens = L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        var marker = L.circleMarker(latlng, {
                            fill: true,
                            fillColor: '#3f9438',
                            fillOpacity: 0.4,
                            radius: 5,
                            stroke: false,
                        });
                        marker.bindPopup(popupTemplate({
                            garden: feature,
                            url: Django.url('farmingconcrete_garden_details', { pk: feature.id })
                        }));
                        return marker;
                    },
                }).addTo(map);
                map.fitBounds(gardens.getBounds());
            });
        }

        $(document).ready(function () {
            var map = initializeMap();
            addOverlay(map);
        });

    }

);
