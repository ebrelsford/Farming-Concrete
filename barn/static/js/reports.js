//
// Reports
//
// Scripts dealing with the reports section of the Barn.
//

var $ = require('jquery');
var Django = require('django');
var moment = require('moment');
var rome = require('rome');
var _ = require('underscore');
require('bootstrap');

function updateDownloadButtonUrl() {
    var url = Django.url('reports_pdf', { pk: $('.pdf-modal :input[name=pk]').val() }),
        params = {},
        dateType = $(':input[name=date_type]:checked').attr('id');

    // Add parameters for date
    if (dateType === 'year') {
        params.year = $(':input[name=year]').val();
    }
    if (dateType === 'range') {
        params.min = moment($(':input[name=min]').val()).format('MM/DD/YYYY');
        params.max = moment($(':input[name=max]').val()).format('MM/DD/YYYY');
    }
    url += '?' + $.param(params);
    $('.pdf-modal .btn-primary').attr('href', url);
}

function updateYearSelect(years) {
    var $yearSelect = $(':input[name=year]');
    $yearSelect.empty();

    $.each(years, function (i, year) {
        var $option = $('<option></option>')
            .val(year)
            .text(year);
        $yearSelect.append($option);
    });

    $yearSelect.find('option').last().prop('selected', true);
}

function updateDateRange(min, max) {
    var options = {
        max: moment(max, 'MM/DD/YYYY'),
        min: moment(min, 'MM/DD/YYYY'),
        time: false
    };
    var minRome = $(':input[name=min]')[0],
        maxRome = $(':input[name=max]')[0];
    rome.find(minRome)
        .options(_.extend({}, options, {
            dateValidator: rome.val.beforeEq(maxRome),
            initialValue: options.min
        }))
        .on('data', function () { updateDownloadButtonUrl(); });
    rome.find(maxRome)
        .options(_.extend({}, options, {
            dateValidator: rome.val.afterEq(minRome),
            initialValue: options.max
        }))
        .on('data', function () { updateDownloadButtonUrl(); });
}

function updateFormInputs(options) {
    updateYearSelect(options.years);
    updateDateRange(options.min, options.max);
}

$(document).ready(function () {
    if ($('.reports-page').length > 0) {
        $('.btn-reports').click(function () {
            if ($(this).data('has-records')) {
                return true;
            }
            else {
                alert($(this).data('no-records-message'));
                return false;
            }
        });

        $('.btn-download-report').click(function () {
            $('.pdf-modal :input[name=pk]').val($(this).data('gardenPk'));
            updateFormInputs($(this).data());
            updateDownloadButtonUrl();
        });

        $('.pdf-modal form :input').change(function () {
            updateDownloadButtonUrl();
        });

        // Once user starts downloading, disable, add a nice message
        $('.pdf-modal .btn-primary').click(function () {
            $(this).addClass('disabled');
            $('.pdf-modal').addClass('is-downloading');
            return true;
        });

        $('.pdf-modal').on('hidden.bs.modal', function () {
            $(this).find('.btn-primary').removeClass('disabled');
            $(this).removeClass('is-downloading');
        });
    }
});
