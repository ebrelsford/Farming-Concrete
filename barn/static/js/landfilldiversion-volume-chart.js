//
// landfilldiversion-volume-chart
//

define(
    [
        // Requirements with exports
        'jquery',
        'd3',
        'django',
    ], function ($, d3, Django) {
        $(document).ready(function () {
            var parseDate = d3.time.format("%Y-%m-%d").parse;

            var margin = {top: 20, right: 20, bottom: 30, left: 50},
                width = $('.landfilldiversion-volume-chart').width() - margin.left - margin.right,
                height = 300;

            var x = d3.time.scale()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

            var line = d3.svg.line()
                .x(function (d) { return x(d.date); })
                .y(function (d) { return y(d.volume); });

            var svg = d3.select('.landfilldiversion-volume-chart').append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            d3.json(Django.url('landfilldiversion_volume_data'), function (error, data) {
                data.forEach(function (d) {
                    d.date = parseDate(d.date);
                    d.volume = d.volume;
                });
                console.log(data);

                x.domain(d3.extent(data, function (d) { return d.date; }));
                y.domain(d3.extent(data, function (d) { return d.volume; }));

                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis)
                    .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Volume");

                svg.append("path")
                    .datum(data)
                    .attr("class", "line")
                    .attr("d", line);
            });
        });

    }

);

