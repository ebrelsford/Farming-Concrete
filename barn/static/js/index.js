//
// index
//

var $ = require('jquery');
var _ = require('underscore');
require('./leaflet.basicmap');

function getMap() {
    return $('body').data('map');
}

function getOverlayOptions() {
    var selectedMembership = $(':input[name=garden-membership]:checked').attr('id'),
        selectedTypes = $('.btn-map-types :input:checked'),
        options = {};
    if (selectedMembership === 'user') {
        options.user_gardens = true;
    }
    if (selectedTypes.length > 0) {
        options.gardentype = _.map(selectedTypes, function (type) {
            return type.id;
        }).join(',');
    }
    return options;
}

$(document).ready(function () {
    if ($('.main-index-page').length > 0) {
        $('#map :input').change(function () {
            getMap().addGardenOverlay(getOverlayOptions());
        });
    }
});
