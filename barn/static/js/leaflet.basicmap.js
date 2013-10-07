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
        'leaflet.cloudmade',
        'leaflet.dataoptions',
        'leaflet.gardenoverlay'

    ], function ($, L) {
        $(document).ready(function () {
            var map = L.map('map');
        });
    }
);
