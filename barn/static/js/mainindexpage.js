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
        'handlebars',

        // Other requirements
        'jquery.spin',
    ], function ($, Django, L, Handlebars) {

        var map;

        function initializeMap() {
            var map = L.map('map', {
                center: [40.71, -73.98],
                zoom: 8
            });
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: '781b27aa166a49e1a398cd9b38a81cdf',
                styleId: '24559'
            }).addTo(map);
            return map;
        }

        function addGardensToMap(map) {
            var url = Django.url('farmingconcrete_gardens_geojson'),
                params = {
                    user_gardens: true,
                };
            url += '?' + $.param(params);

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
            map = initializeMap();
            addGardensToMap(map);
        });

    }
);
