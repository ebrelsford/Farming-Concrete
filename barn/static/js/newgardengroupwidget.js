//
// newgardengroupwidget
//

var $ = require('jquery');
var NewInstanceWidget = require('./new_widget');

var NewGardenGroupWidget = NewInstanceWidget.extend({});

$(document).ready(function () {
    if ($('.btn-new-gardengroup').length > 0) {
        var widget = new NewGardenGroupWidget({
            buttonSelector: '.btn-new-gardengroup',
            selectSelector: 'select[name=groups]'
        });
    }
});
