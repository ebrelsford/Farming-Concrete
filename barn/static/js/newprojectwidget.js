//
// newprojectwidget
//
// Supporting script for metrics.participation.forms.AddNewProjectWidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',
        'new_widget',

        // Other requirements
        'jquery.form',
    ], function ($, Django, NewInstanceWidget) {

        var NewProjectWidget = NewInstanceWidget.extend({

            preSubmit: function ($modal) {
                // Ensure the garden input is set
                var gardenPk = $(':input[name=garden][value!=""]').val();
                $modal.find(':input[name=garden]').val(gardenPk);
            }

        });

        $(document).ready(function () {
            var widget = new NewProjectWidget({
                buttonSelector: '.btn-participation-new-project',
                errorMessage: 'There was an error while adding your project. Please try again.',
                selectSelector: 'select[name=project]'
            });
        });

    }
);
