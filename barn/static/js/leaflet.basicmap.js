// leaflet.basicmap
//
// Set up basic map that will work on most pages.
//

define(
    [
        // Requirements with exports
        'jquery',
        'leaflet',

        // Requirements without exports
        'leaflet.dataoptions',
        'leaflet.gardenoverlay',
        'leaflet.mapbox'

    ], function ($, L) {
        $(document).ready(function () {
            var map = L.map('map');
            map.attributionControl.setPrefix('');
        });
    }
);
