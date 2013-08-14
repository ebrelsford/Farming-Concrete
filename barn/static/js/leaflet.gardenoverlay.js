//
// leaflet.gardenoverlay
//
// A Leaflet plugin that automatically adds a garden overlay to a map.
//

define(
    [
        'django',
        'jquery',
        'handlebars',
        'leaflet',
        'underscore',

    ], function (Django, $, Handlebars, L, _) {
        var mapParams = ['cropcount', 'gardentype', 'year'],
            style = {
                fill: true,
                fillColor: '#3f9438',
                fillOpacity: 0.4,
                radius: 5,
                stroke: false,
            };

        L.Map.include({

            addGardenOverlay: function () {
                var instance = this,
                    url = Django.url('farmingconcrete_gardens_geojson');
                url += '?' + $.param(_.pick(instance.options, mapParams));
                $.getJSON(url, function (data) {
                    instance.addGardenData(data);
                });
            },

            addGardenData: function (data) {
                var instance = this,
                    popupTemplate = Handlebars.compile($('#popup-template').html());

                var gardens = L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        var marker = L.circleMarker(latlng, style);
                        marker.bindPopup(popupTemplate({
                            garden: feature,
                            url: Django.url('farmingconcrete_garden_details', { pk: feature.id })
                        }));
                        return marker;
                    },
                }).addTo(instance);
                instance.fitBounds(gardens.getBounds());
            }

        });

        L.Map.addInitHook(function () {
            this.addGardenOverlay();
        });
    }
);
