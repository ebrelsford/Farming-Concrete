//
// addgardengroupadmin
//

var $ = require('jquery');
var Django = require('django');

$(document).ready(function () {
    if ($('.add-garden-group-admin').length > 0) {
        // TODO CSS seems funky here
        $(':input#id_users')
            .addClass('select2-basic-select')
            .select2();
    }
});
