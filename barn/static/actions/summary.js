(function () {
    function actionsSummaryOnReady() {
        setTimeout(function () {
            qwest.get('../api-admin/actions/summary/')
                .then(function (xhr, data) {
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
                                tick: {
                                    format: '%m/%Y'
                                },
                                type: 'timeseries'
                            }
                        },
                        bar: {
                            width: {
                                ratio: 0.5
                            }
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
                        size: {
                            width: width
                        },
                    });
                    chart.show();
                });
        }, 1000);
    }

    if (document.readyState !== 'loading') {
        actionsSummaryOnReady();
    }
    else {
        document.addEventListener('DOMContentLoaded', actionsSummaryOnReady);
    }
})();
