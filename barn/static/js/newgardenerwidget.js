//
// newgardenerwidget
//
// Supporting script for metrics.harvestcount.forms.AddNewGardenerWidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',
        'new_widget',

        // Other requirements
        'jquery.form'
    ], function ($, Django, NewInstanceWidget) {

        var NewGardenerWidget = NewInstanceWidget.extend({

            preSubmit: function ($modal) {
                // Ensure the garden input is set
                var gardenPk = $(':input[name=garden][value!=""]').val();
                $modal.find(':input[name=garden]').val(gardenPk);
            }

        });

        $(document).ready(function () {
            var widget = new NewGardenerWidget({
                buttonSelector: '.btn-new-gardener',
                errorMessage: 'There was an error while adding your gardener. Please try again.',
                selectSelector: 'select[name=gardener]'
            });
        });

    }
);
