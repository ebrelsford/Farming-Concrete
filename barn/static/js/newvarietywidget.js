//
// newvarietywidget
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',

        // Other requirements
        'jquery.form',
    ], function ($, Django) {

        function addModal() {
            // Add our modal to the end of the body to reduce potential nested
            // forms confusion
            $('body').append(
                $('<div></div>')
                    .attr('id', 'new-variety-modal')
                    .attr('class', 'modal')
            );
            return $('#new-variety-modal');
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

        var inputName = 'variety';

        function submitForm($modal, e) {
            // Ensure the input is set
            var pk = $(':input[name=' + inputName + '][value!=""]').val();
            $modal.find(':input[name=' + inputName + ']').val(pk);

            var $form = $modal.find('form'),
                $nameInput = $form.find(':input[name=name]');

            if ($nameInput.val() !== '') {
                // If we have a name for the entity, attempt to submit
                $form.ajaxSubmit({
                    error: function () {
                        addError($nameInput, 'There was an error while adding. Please try again.');
                    },
                    success: function (data) {
                        var $select = $('select[name=' + inputName + ']'),
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
                        $select.trigger('change');
                    }
                });
            }
            else {
                // Let the user know that we need a name to submit
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
