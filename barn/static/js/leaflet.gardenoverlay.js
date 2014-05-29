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
        'prefixurl'
    ], function ($, Handlebars, L, _, prefixurl) {
        var mapParams = [
            'cropcount',
            'gardenid',
            'gardentype',
            'ids',
            'metric',
            'user_gardens',
            'year'
        ];

        var style = {
            fill: true,
            fillColor: '#F63C04',
            fillOpacity: 0.4,
            radius: 15,
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

            addGardenOverlay: function () {
                var instance = this,
                    url = prefixurl.url('farmingconcrete_gardens_geojson');
                url += '?' + $.param(_.pick(instance.options, mapParams));
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

                var gardens = L.geoJson(data, {
                    pointToLayer: function (feature, latlng) {
                        var marker = L.circleMarker(latlng, style);
                        marker.bindPopup(popupTemplate({
                            garden: feature,
                            url: prefixurl.url('farmingconcrete_garden_details', { pk: feature.id })
                        }));
                        return marker;
                    },
                }).addTo(instance);
                instance.fitBounds(gardens.getBounds());

                // If we're only looking at one garden, zoom out a bit
                if (gardens.getLayers().length === 1) {
                    instance.setZoom(14);
                }
            }

        });

        L.Map.addInitHook(function () {
            this.addGardenOverlay();
        });
    }
);
