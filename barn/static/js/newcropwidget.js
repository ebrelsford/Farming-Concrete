//
// newcropwidget
//

var $ = require('jquery');
var NewInstanceWidget = require('./new_widget');

var NewCropWidget = NewInstanceWidget.extend({});

$(document).ready(function () {
    if ($('.btn-new-crop').length > 0) {
        var widget = new NewCropWidget({
            buttonSelector: '.btn-new-crop',
            selectSelector: 'select[name=crop],select[name$=crop]'
        });
    }
});
