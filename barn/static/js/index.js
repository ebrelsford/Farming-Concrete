//
// index
//

define(['jquery'], function ($) {

    function getMap() {
        return $('body').data('map');
    }

    $(document).ready(function () {
        $(':input[name=garden-membership]').change(function () {
            var selected = $(this).attr('id'),
                options = {};
            if (selected === 'user') {
                options.user_gardens = true;
            }
            getMap().addGardenOverlay(options);
        });
    });
});
