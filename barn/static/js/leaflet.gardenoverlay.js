//
// leaflet.gardenoverlay
//
// A Leaflet plugin that automatically adds a garden overlay to a map.
//

define(
    [
        'jquery',
        'handlebars',
        'leaflet',
        'underscore',
        'django'
    ], function ($, Handlebars, L, _, Django) {
        var mapParams = [
            'cropcount',
            'gardenid',
            'gardentype',
            'group',
            'ids',
            'metric',
            'user_gardens',
            'year'
        ];

        var style = {
            fill: true,
            fillColor: '#F63C04',
            fillOpacity: 0.7,
            radius: 5,
            stroke: false
        };

        var individualGardenStyle = {
            fill: true,
            fillColor: '#F54613',
            fillOpacity: 0.8,
            radius: 25,
            stroke: false
        };

        L.Map.include({

            addGardenOverlay: function (options) {
                var instance = this,
                    url = Django.url('farmingconcrete_gardens_geojson');
                options = options || instance.options;
                url += '?' + $.param(_.pick(options, mapParams));
                $.getJSON(url, function (data) {
                    instance.addGardenData(data);
                });
            },

            pickStyle: function () {
                var instance = this;
                if (instance.options.gardenid) {
                    return individualGardenStyle;
                }
                return style;
            },

            addGardenData: function (data) {
                var instance = this,
                    popupTemplate = Handlebars.compile($('#popup-template').html()),
                    style = instance.pickStyle();

                if (instance.gardens) {
                    instance.removeLayer(instance.gardens);
                }
                instance.gardens = L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        var marker = L.circleMarker(latlng, style);
                        marker.bindPopup(popupTemplate({
                            garden: feature,
                            url: Django.url('farmingconcrete_garden_details', { pk: feature.id })
                        }));
                        return marker;
                    },
                }).addTo(instance);

                // If there is anything mapped, fit map to it
                if (instance.gardens.getLayers().length > 0) {
                    instance.fitBounds(instance.gardens.getBounds(), {
                        padding: [50, 50]
                    });
                }
            }

        });

        L.Map.addInitHook(function () {
            this.addGardenOverlay();
        });
    }
);
