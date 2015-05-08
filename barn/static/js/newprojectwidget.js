//
// newprojectwidget
//
// Supporting script for metrics.participation.forms.AddNewProjectWidget
//

var $ = require('jquery');
var Django = require('django');
var NewInstanceWidget = require('./new_widget');
require('jquery-form/jquery.form');

var NewProjectWidget = NewInstanceWidget.extend({

    preSubmit: function ($modal) {
        // Ensure the garden input is set
        var gardenPk = $(':input[name=garden][value!=""]').val();
        $modal.find(':input[name=garden]').val(gardenPk);
    }

});

$(document).ready(function () {
    if ($('.btn-new-project').length > 0) {
        var widget = new NewProjectWidget({
            buttonSelector: '.btn-new-project',
            errorMessage: 'There was an error while adding your project. Please try again.',
            selectSelector: 'select[name=project]'
        });
    }
});
