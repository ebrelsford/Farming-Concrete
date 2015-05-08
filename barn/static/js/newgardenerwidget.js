//
// newgardenerwidget
//
// Supporting script for metrics.harvestcount.forms.AddNewGardenerWidget
//

var $ = require('jquery');
var Django = require('django');
var NewInstanceWidget = require('./new_widget');
require('jquery-form/jquery.form');

var NewGardenerWidget = NewInstanceWidget.extend({

    getSelector: function ($button) {
        return $button.parent().find('select');
    },

    preSubmit: function ($modal) {
        // Ensure the garden input is set
        var gardenPk = $(':input[name=garden][value!=""]').val();
        $modal.find(':input[name=garden]').val(gardenPk);
    }

});

$(document).ready(function () {
    if ($('.btn-new-gardener').length > 0) {
        var widget = new NewGardenerWidget({
            buttonSelector: '.btn-new-gardener',
            selectSelector: 'select[name$=gardener]',
            errorMessage: 'There was an error while adding your gardener. Please try again.'
        });
    }
});
