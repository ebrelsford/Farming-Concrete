//
// addgardengroupadmin
//

define(['jquery', 'django', 'select2'], function ($, Django) {

    $(document).ready(function () {
        // TODO CSS seems funky here
        $(':input#id_users')
            .addClass('select2-basic-select')
            .select2();
    });

});
