//
// Reports
//
// Scripts dealing with the reports section of the Barn.
//

define(['jquery', 'django', 'bootstrap'], function ($, Django) {

    function updateDownloadButtonUrl() {
        var url = Django.url('reports_pdf', { pk: $('.pdf-modal :input[name=pk]').val() }),
            params = {},
            dateType = $(':input[name=date_type]:checked').attr('id');;

        // Add parameters for date
        if (dateType === 'year') {
            params.year = $(':input[name=year]').val();
        }
        if (dateType === 'range') {
            params.min = $(':input[name=min]').val();
            params.max = $(':input[name=max]').val();
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
        var setParams = { format: 'mm/dd/yyyy' };
        $(':input[name=min]').data('pickadate').set('select', min, setParams);
        $(':input[name=max]').data('pickadate').set('select', max, setParams);
    }

    function updateFormInputs(options) {
        updateYearSelect(options.years);
        updateDateRange(options.min, options.max);
    }

    $(document).ready(function () {
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
    });

});
