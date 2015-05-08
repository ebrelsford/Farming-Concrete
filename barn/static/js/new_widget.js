//
// new_widget
//

var $ = require('jquery');
var _ = require('underscore');
var Class = require('resig-class');

require('jquery-form/jquery.form');

var NewInstanceWidget = Class.extend({

    options: {
        buttonSelector: '',
        errorMessage: 'There was an error while adding. Please try again.',
        selectSelector: ''
    },

    init: function (options) {
        this.options = _.extend({}, this.options, options);
        var t = this,
            modalId = $(this.options.buttonSelector).data('target'),
            $modal;
        if (modalId) {
            modalId = modalId.slice(1);
            $modal = t.addModal(modalId);
        }
        t.$select = null;

        // Get the select element when a button is clicked, potentially
        // in relation to the clicked button
        $(document.body).on('click', this.options.buttonSelector, function () {
            t.$select = t.getSelector($(this));
            return true;
        });

        // Hide modal when cancel button is clicked
        $modal.on('click', function (event) {
            if ($(event.target).hasClass('btn-cancel')) {
                $modal.modal('hide');
            }
        });

        // Focus on first input element on load. Only works the first
        // time, but hopefully that's good enough
        $modal.on('loaded.bs.modal', function () {
            $('.modal:visible form :input:visible:eq(0)').focus();
        });

        // Submit form when submitted
        $modal.on('submit', function (e) {
            return t.submitForm($modal, t.$select, e);
        });
        return this;
    },

    getSelector: function ($button) {
        // TODO this is getting confused, new variety in gardener select
        var t = this,
            select = $(t.options.selectSelector);
        if (select.length > 1) {
            select = $button.parent().find(t.options.selectSelector);
        }
        return select;
    },

    addModal: function (id) {
        // Add our modal to the end of the body to reduce potential nested
        // forms confusion
        $('body').append(
            $('<div></div>')
                .attr('id', id)
                .attr('class', 'modal')
                .append(
                    $('<div></div>')
                        .attr('class', 'modal-dialog')
                        .append(
                            $('<div></div>')
                                .attr('class', 'modal-content')
                        )
                )
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
                    if ($select.find('.select2-basic-select').length > 0) {
                        $select.select2('data', { id: data.pk, text: data.name });
                    }
                    else {
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
                    $modal.modal('hide');
                }
            });
        }
        else {
            // Let the user know that we need a name to submit
            t.addError($nameInput, 'Please enter a name');
            event.stopPropagation();
            return false;
        }
        return false;
    }

});

module.exports = NewInstanceWidget;
