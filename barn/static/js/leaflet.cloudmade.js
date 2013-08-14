//
// leaflet.cloudmade
//
// A Leaflet plugin that simplifies adding a cloudmade base layer to a map.
//

define(['leaflet'], function (L) {

    L.Map.include({

        addCloudmadeLayer: function () {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: this.options.apikey,
                styleId: this.options.styleid
            }).addTo(this);
        }

    });

    L.Map.addInitHook(function () {
        this.addCloudmadeLayer();
    });

});
