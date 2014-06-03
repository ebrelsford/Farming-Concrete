//
// newvarietywidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'new_widget'

    ], function ($, NewInstanceWidget) {

        var NewVarietyWidget = NewInstanceWidget.extend({});

        $(document).ready(function () {
            var widget = new NewVarietyWidget({
                buttonSelector: '.btn-new-variety',
                selectSelector: 'select[name=variety],select[name=vegetable]'
            });
        });

    }
);
