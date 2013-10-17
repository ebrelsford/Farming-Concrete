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

        function addModal(id) {
            // Add our modal to the end of the body to reduce potential nested
            // forms confusion
            $('body').append(
                $('<div></div>')
                    .attr('id', id)
                    .attr('class', 'modal')
            );
            return $('#' + id);
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

        function submitForm($modal, $select, event) {
            var $form = $modal.find('form'),
                $nameInput = $form.find(':input[name=name]');

            if ($nameInput.val() !== '') {
                // If we have a name for the entity, attempt to submit
                $form.ajaxSubmit({
                    error: function () {
                        addError($nameInput, 'There was an error while adding. Please try again.');
                    },
                    success: function (data) {
                        var $existing = $select.find('option[value=' + data.pk + ']');
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
                event.stopPropagation();
                return false;
            }
            $modal.modal('hide');
            return false;
        }

        $(document).ready(function () {
            var id = $('.btn-new-variety').data('target').slice(1),
                $modal = addModal(id),
                $select = $('select[name=variety]');

            // Hide modal when cancel button is clicked
            $modal.on('click', function (event) {
                if ($(event.target).hasClass('btn-cancel')) {
                    $modal.modal('hide');
                }
            });

            // Submit form when submitted
            $modal.on('submit', function (e) {
                return submitForm($modal, $select, e);
            });

        });

    }
);
