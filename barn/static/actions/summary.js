(function () {
    var endpoint = '../api-admin/actions/summary/',
        dateFormat = 'YYYY-MM-DD';

    function createChart(data) {
        var countsColumn = ['counts'];
        _.each(data.counts, function (count) {
            return countsColumn.push(count.count);
        });

        var xTicks = ['x'];
        _.each(data.counts, function (count) {
            xTicks.push(new Date(count.year, count.month));
        });

        var width = document.getElementById('actions-summary-chart').offsetWidth;
        var chart = c3.generate({
            axis: {
                x: {
                    tick: { format: '%m/%Y' },
                    type: 'timeseries'
                }
            },
            bar: {
                width: { ratio: 0.5 }
            },
            bindto: '#actions-summary-chart',
            data: {
                columns: [
                    xTicks,
                    countsColumn
                ],
                type: 'bar',
                x: 'x'
            },
            size: { width: width },
        });
        chart.show();
    }

    function updateChart() {
        var now = moment(new Date()),
            lastYear = now.clone().subtract(1, 'years'),
            minTimestamp = lastYear.format(dateFormat),
            maxTimestamp = now.format(dateFormat);

        var verbOptions = document.querySelectorAll('.actions-summary-filters-verb option');
        var verbs = _.chain(verbOptions)
            .filter(function (option) {
                return option.selected;
            })
            .map(function (option) {
                return 'verb=' + option.value;
            });

        qwest.get(endpoint + '?' + verbs.join('&'), {
            'max_timestamp': maxTimestamp,
            'min_timestamp': minTimestamp
        })
            .then(function (xhr, data) {
                createChart(data);
            });
    }

    function actionsSummaryOnReady() {
        var select = document.querySelectorAll('.actions-summary-filters-verb')[0];
        actionVerbs.forEach(function (verb) {
            var option = document.createElement('option');
            option.setAttribute('value', verb);
            option.textContent = verb;
            select.appendChild(option);
        });

        select.addEventListener('change', function () {
            updateChart();
        });

        setTimeout(function () {
            updateChart();
        }, 1000);
    }

    if (document.readyState !== 'loading') {
        actionsSummaryOnReady();
    }
    else {
        document.addEventListener('DOMContentLoaded', actionsSummaryOnReady);
    }
})();
