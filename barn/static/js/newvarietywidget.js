//
// newvarietywidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'new_widget'

    ], function ($, NewInstanceWidget) {

        // TODO make work with crops.Crop / crops.Variety
        var NewVarietyWidget = NewInstanceWidget.extend({});

        $(document).ready(function () {
            var widget = new NewVarietyWidget({
                buttonSelector: '.btn-new-variety',
                selectSelector: 'select[name=variety],select[name=vegetable],' +
                    'select[name$=variety]'
            });
        });

    }
);
