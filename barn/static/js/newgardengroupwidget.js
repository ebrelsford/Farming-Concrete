//
// newgardengroupwidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'new_widget'

    ], function ($, NewInstanceWidget) {
        var NewGardenGroupWidget = NewInstanceWidget.extend({});

        $(document).ready(function () {
            var widget = new NewGardenGroupWidget({
                buttonSelector: '.btn-new-gardengroup',
                selectSelector: 'select[name=groups]'
            });
        });
    }
);
