//
// newcropwidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'new_widget'

    ], function ($, NewInstanceWidget) {

        var NewCropWidget = NewInstanceWidget.extend({});

        $(document).ready(function () {
            var widget = new NewCropWidget({
                buttonSelector: '.btn-new-crop',
                selectSelector: 'select[name=crop],select[name$=crop]'
            });
        });

    }
);
