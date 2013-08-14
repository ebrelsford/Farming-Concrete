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

        // Requirements without exports
        'leaflet.dataconfig'

    ], function ($, L) {
        
        var map;

        function initializeMap() {
            var map = L.map('map');
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
            return map;
        }

        $(document).ready(function () {
            initializeMap();
        });

    }

);
