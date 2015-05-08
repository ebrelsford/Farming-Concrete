//
// feedback
//
// Feedback button + form
//

require('jquery-form/jquery.form');
// TODO make this work?
var Spinner = require('spin.js');

function initializeFeedbackForm() {

    $('#feedback-button').click(function () {
        $('#feedback-button').slideUp(function () {
            $('#feedback-form').slideDown();
        });
    });

    $('#feedback-form .btn-cancel').click(function () {
        $('#feedback-form').slideUp(function () {
            $('#feedback-button').slideDown();
        });
    });

    $('#feedback-form form').submit(function () {
        $('#feedback-form')
            .addClass('is-loading')
            .spin('large');
        $(this).ajaxSubmit({
            data: {
                next: Django.url('feedback_success'),
            },
            success: function () {
                $('#feedback-form')
                    .removeClass('is-loading')
                    .spin(false);
                initializeFeedbackForm();
            },
            target: '#feedback-form'
        });
        return false;
    });

}

$(document).ready(function () {
    initializeFeedbackForm();
});
