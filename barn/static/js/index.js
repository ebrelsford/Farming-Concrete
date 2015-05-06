//
// index
//

define(['jquery', 'underscore'], function ($, _) {

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
        $('#map :input').change(function () {
            getMap().addGardenOverlay(getOverlayOptions());
        });
    });
});
