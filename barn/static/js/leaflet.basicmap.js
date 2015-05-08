// leaflet.basicmap
//
// Set up basic map that will work on most pages.
//

var $ = require('jquery');
var L = require('leaflet');

require('leaflet.dataoptions');
require('./leaflet.gardenoverlay');
require('./leaflet.mapbox');

$(document).ready(function () {
    if ($('#map').length > 0) {
        var map = L.map('map');
        map.attributionControl.setPrefix('');

        // Put the map somewhere we can access it later
        $('body').data('map', map);
    }
});
