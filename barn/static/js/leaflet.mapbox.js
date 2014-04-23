//
// leaflet.mapbox
//
// A Leaflet plugin that simplifies adding a Mapbox base layer to a map.
//

define(['leaflet'], function (L) {

    L.Map.include({

        addMapboxLayer: function () {
            L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                mapboxId: this.options.mapboxId
            }).addTo(this);
        }

    });

    L.Map.addInitHook(function () {
        this.addMapboxLayer();
    });

});