//
// index
//

define(['jquery'], function ($) {

    function getMap() {
        return $('body').data('map');
    }

    $(document).ready(function () {

        $('.btn-map-user-gardens').click(function () {
            getMap().addGardenOverlay({user_gardens: true});
            return false;
        });

        $('.btn-map-all-gardens').click(function () {
            getMap().addGardenOverlay({});
            return false;
        });

    });
});
