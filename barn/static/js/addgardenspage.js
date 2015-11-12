//
// addgardenspage
//
// Scripts for the add gardens page.
//

var $ = require('jquery');
var Django = require('django');
var L = require('leaflet');
var geocode = require('./geocode');
var _ = require('underscore');
var Spinner = require('spin.js');

require('bootstrap');
require('jquery-form/jquery.form');
require('leaflet.dataoptions');
require('leaflet-usermarker');
require('./newgardengroupwidget');

var map,
    gardenMarker;

function updateSuggestions() {
    var baseUrl = Django.url('farmingconcrete_gardens_suggest'),
        name = $('#id_name').val(),
        $wrapper = $('.garden-suggestions-wrapper'),
        spinner = new Spinner().spin($wrapper[0]);
    $wrapper
        .addClass('is-loading')
        .load(baseUrl + '?' + $.param({ name: name }), function () {
            spinner.stop();
            $wrapper
                .removeClass('is-loading');
            activateSuggestedGardens();
        });
}

function clearSuggestions() {
    $('.garden-suggestions-wrapper').empty();
}

function activateSuggestedGardens() {
    $('.garden-suggestion').click(function () {
        selectSuggestedGarden($(this).data('pk'));
    });
}

function initializeMap() {
    var map = L.map('add-garden-map');
    L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        mapboxId: map.options.mapboxId
    }).addTo(map);
    return map;
}

function selectSuggestedGarden(pk) {
    window.location.href = Django.url('farmingconcrete_gardens_suggest_add', { 'pk': pk });
}

function geocodeAddress() {
    var address = $('#id_address').val(),
        city = $('#id_city').val(),
        state = $('#id_state').val(),
        country = $('#id_country').val(),
        postal_code = $('#id_zip').val(),
        components = _.filter([address, city, state, country, postal_code],
                function (c) { return c !== ''; });

    if (components.length >= 3) {
        geocode.geocode(components.join(','), state, function (result, status) {
            if (status === 'OK' && result) {
                showGeocodedResultOnMap(result);
            }
        });
    }
}

function roundCoordinate(c) {
    return Math.round(c * 10000) / 10000;
}

function setGardenLocation(result) {
    var lat = geocode.get_latitude(result),
        lng = geocode.get_longitude(result);
    $('#id_latitude').val(roundCoordinate(lat));
    $('#id_longitude').val(roundCoordinate(lng));
    $('#id_address').val(geocode.get_street(result));
    $('#id_neighborhood').val(geocode.get_neighborhood(result));
    $('#id_city').val(geocode.get_city(result));
    $('#id_state').val(geocode.get_state(result));
    $('#id_country').val(geocode.get_country(result));
    $('#id_zip').val(geocode.get_zip(result));

    var borough = geocode.get_borough(result),
        $boroughOption = $('#id_borough option[value="' + borough + '"]');
    if ($boroughOption.length > 0) {
        $boroughOption
            .prop('selected', true)
            .parents('.form-group').show();
    }
}

function showPointOnMap(lat, lng, result) {
    var latlng = [lat, lng];
    if (gardenMarker) {
        map.removeLayer(gardenMarker);
    }
    gardenMarker = L.userMarker(latlng, { smallIcon: true }).addTo(map);
    map.setView(latlng, 15);
}

function showPointPopup(lat, lng, result) {
    if (roundCoordinate(lat) !== parseFloat($('#id_latitude').val()) || roundCoordinate(lng) !== parseFloat($('#id_longitude').val())) {
        var popupContent = 'This is the point we found. Use this address? <a href="#" class="btn btn-default btn-use-address">Ok</a>.';
        gardenMarker.bindPopup(popupContent, { maxWidth: 100 }).openPopup();
    }

    $('.btn-use-address').click(function () {
        setGardenLocation(result)
        gardenMarker.closePopup();
        return false;
    });
}

function showGeocodedResultOnMap(result) {
    var lat = geocode.get_latitude(result),
        lng = geocode.get_longitude(result);
    showPointOnMap(lat, lng, result);
    showPointPopup(lat, lng, result);
}

$(document).ready(function () {
    if ($('.add-gardens-page').length > 0) {
        map = initializeMap();

        var lat = $('#id_latitude').val(),
            lng = $('#id_longitude').val();
        if (lat && lng) {
            showPointOnMap(lat, lng);
            map.setView([lat, lng], 16);
        }

        $('form.add-garden').on('submit', function () {
            var latitude = $(this).find('[name=latitude]').val(),
                longitude = $(this).find('[name=longitude]').val();

            if (!latitude || !longitude) {
                $('.add-garden-map-error').show();
                return false;
            }
        });

        // If creating a new garden, enable suggestions
        if ($('.garden-form').is('.add-garden')) {
            // If name already has text in it (eg on error), show
            // suggestions
            if ($('#id_name').val().length >= 3) {
                updateSuggestions();
            }
            $('#id_name').keyup(function () {
                if ($(this).val().length >= 3) {
                    updateSuggestions();
                }
                else {
                    clearSuggestions();
                }
            });
        }

        $('#id_address,#id_city,#id_state,#id_country').change(geocodeAddress);

        $('#invite-member-modal').on('shown.bs.modal', function () {
            var $modal = $(this);

            $modal.find(':input[name=garden]').val($modal.data('garden'));

            $modal.find('.btn-cancel').click(function () {
                $('#invite-member-modal').modal('hide');
            });

            $modal.find('form').on('submit', function (e) {
                var $form = $(this),
                    email = $form.find(':input[name=email]').val();
                $modal.removeClass('error success');

                // This could be handled more nicely, but seriously?
                if (!email) return false;

                $form.ajaxSubmit({
                    error: function () {
                        $modal.addClass('error');
                    },
                    success: function (data) {
                        $modal.addClass('success');
                        $('#invited-email-address').text(email);
                        $form.find(':input[name=email]').val('');
                    }
                });
                return false;
            });
        });

        $('[data-toggle="tooltip"]').tooltip();

        // Request permission to join a group
        $('.request-group-permission').click(function (e) {
            e.preventDefault();
            if ($(this).hasClass('loading')) {
                return false;
            }
            var $message = $(this).parents('.group-permission-required-message');
            var $loading = $('<span></span>')
                .css({
                    display: 'inline-block',
                    width: '15px',
                    height: '15px' 
                });
            $message.append($loading);

            var spinner = new Spinner({
                color: '#000',
                left: 0,
                length: 4,
                radius: 3,
                top: 0,
                width: 1
            }).spin($loading[0]);

            // Disable link
            $(this).addClass('loading');
            $.getJSON($(this).attr('href'))
                .done(function (data) {
                    if (data.request_sent === true) {
                        $message.append(
                            $('<p></p>')
                                .text('Request sent.')
                        );
                    }
                    else {
                        $message.append(
                            $('<p></p>')
                                .text('Request not sent. ' + data.message)
                        );
                    }
                })
                .fail(function () {
                    $message.append(
                        $('<p></p>')
                            .text('There was an error while sending your request. Please try again later and let us know if this continues.')
                    );
                })
                .always(function () {
                    spinner.stop();
                    $loading.remove();
                    $message.addClass('request-sent');
                });
            return false;
        });
    }
});
