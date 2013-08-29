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

        // Other requirements
        'jquery.form',
        'jquery.spin',
    ], function ($, Django) {

        function addModal() {
            // Add our modal to the end of the body to reduce potential nested
            // forms confusion
            $('body').append(
                $('<div></div>')
                    .attr('id', 'new-project-modal')
                    .attr('class', 'modal')
            );
            return $('#new-project-modal');
        }

        function addError($nameInput, msg) {
            var $formGroup = $nameInput.parents('.form-group');

            // Only add the error once if we can help it
            if (!$formGroup.hasClass('has-error')) {
                $formGroup.addClass('has-error');
                $nameInput.after(
                    $('<div></div>')
                        .addClass('help-block')
                        .html(msg)
                );
            }
        }

        function submitForm($modal, e) {
            // Ensure the garden input is set
            var gardenPk = $(':input[name=garden][value!=""]').val();
            $modal.find(':input[name=garden]').val(gardenPk);

            var $form = $modal.find('form'),
                $nameInput = $form.find(':input[name=name]');

            if ($nameInput.val() !== '') {
                // If we have a name for the project, attempt to submit
                $form.ajaxSubmit({
                    error: function () {
                        addError($nameInput, 'There was an error while adding your project. Please try again.');
                    },
                    success: function (data) {
                        var $select = $('select[name=project]'),
                            $existing = $select.find('option[value=' + data.pk + ']');
                        if ($existing.length > 0) {
                            $existing.prop('selected', true);
                        }
                        else {
                            var newOption = $('<option></option>')
                                .attr('value', data.pk)
                                .prop('selected', true)
                                .html(data.name);
                            $select.append(newOption);
                        }
                    }
                });
            }
            else {
                // Let the user know that we need a project name to submit
                addError($nameInput, 'Please enter a name');
                e.stopPropagation();
                return false;
            }
            $modal.modal('hide');
            return false;
        }

        $(document).ready(function () {

            var $modal = addModal();

            // Hide modal when cancel button is clicked
            $modal.on('click', function (event) {
                if ($(event.target).hasClass('btn-cancel')) {
                    $modal.modal('hide');
                }
            });

            // Submit form when submitted
            $modal.on('submit', function (e) {
                return submitForm($modal, e);
            });

        });

    }

);
