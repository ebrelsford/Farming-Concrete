//
// new_widget
//

define(
    [
        // Requirements with exports
        'jquery',
        'underscore',
        'resig-class',

        // Other requirements
        'jquery.form',
    ], function ($, _, Class) {

        var NewInstanceWidget = Class.extend({

            options: {
                buttonSelector: '',
                errorMessage: 'There was an error while adding. Please try again.',
                selectSelector: ''
            },

            init: function (options) {
                this.options = _.extend(this.options, options);
                var t = this,
                    id = $(t.options.buttonSelector).data('target'),
                    $modal;
                if (id) {
                    id = id.slice(1);
                    $modal = t.addModal(id);
                }
                var $select = $(t.options.selectSelector);

                // Hide modal when cancel button is clicked
                $modal.on('click', function (event) {
                    if ($(event.target).hasClass('btn-cancel')) {
                        $modal.modal('hide');
                    }
                });

                // Submit form when submitted
                $modal.on('submit', function (e) {
                    return t.submitForm($modal, $select, e);
                });
            },

            addModal: function (id) {
                // Add our modal to the end of the body to reduce potential nested
                // forms confusion
                $('body').append(
                    $('<div></div>')
                        .attr('id', id)
                        .attr('class', 'modal')
                );
                return $('#' + id);
            },

            addError: function ($nameInput, msg) {
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
            },

            preSubmit: function ($modal) {
                // Nothing. Placeholder to be overridden as needed
            },

            submitForm: function ($modal, $select, event) {
                var t = this,
                    $form = $modal.find('form'),
                    $nameInput = $form.find(':input[name=name]');

                t.preSubmit($modal);

                if ($nameInput.val() !== '') {
                    // If we have a name for the entity, attempt to submit
                    $form.ajaxSubmit({
                        error: function () {
                            t.addError($nameInput, t.options.errorMessage);
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
                    t.addError($nameInput, 'Please enter a name');
                    event.stopPropagation();
                    return false;
                }
                $modal.modal('hide');
                return false;
            }

        });

        return NewInstanceWidget;
    }
);
