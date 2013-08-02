var map;

function get_selected_value(s) {
    if (s.attr('class') == 'all') return null;
    return s.val();
}

function on_update(results) {
    // update map
    map.highlightGardens(results.gardens);

    // update legend
    var total_plants = results.plants;
    var sq_ft = results.area;
    $('#stats #gardens .value').text(results.gardens.length);

    if (sq_ft) {
        var acres = (sq_ft / 43560).toPrecision(2);
        $('#stats #area .value').text(acres + ' acres (' + number_format(sq_ft) + ' sq ft)');
    }
    else {
        $('#stats #area .value').text('-');
    }
    $('#stats #plants .value').text(number_format(total_plants));
    $('#stats #pounds .value').text(number_format(results.pounds));
    $('#stats #money .value').text('$' + number_format(results.cost, 2));

    // update statement
    var place_name = 'New York City';
    var borough = get_selected_value($('.borough:visible option:selected'));
    var neighborhood = get_selected_value($('.neighborhood:visible option:selected'));
    var year = get_selected_value($('#year option:selected'));

    if (borough) {
        if (neighborhood) {
            place_name = neighborhood + ', ' + borough;
        }
        else {
            place_name = borough;
        }
    }
    else if (neighborhood) {
        place_name = neighborhood;
    }

    var variety_name = 'food';
    var variety = get_selected_value($('.vegetables:visible option:selected'));
    if (variety) variety_name = variety;

    $('#statement .gardens').text(results.gardens.length);
    $('#statement .location').text(place_name);
    $('#statement .pounds').text(number_format(results.pounds));
    $('#statement .money').text(number_format(results.cost));
    $('#statement .variety').text(variety_name);
    $('#statement .year').text(year);

    $('#update_loading_indicator').hide();
}

function get_selected_option(id) {
    $option = $('.' + id + ':visible option:selected');
    if ($option.attr('class') == 'all')
        return 'all';
    return $option.val();
}

/*
 * Keep hidden selectors synchronized with the visible ones.
 */
function sync_hidden_selects(select_class, value) {
    $(':input.' + select_class + ':hidden option[value="' + value + '"]').attr('selected', 'selected');
}

function get_query_data() {
    return {
        borough: get_selected_option('borough'),
        neighborhood: get_selected_option('neighborhood'),
        variety: get_selected_option('vegetables'),
        year: $('#year option:selected').val(),
    };
    return query_data;
}

function submit_query() {
    $.getJSON('/harvestmap/data/harvests?', get_query_data(), on_update);
    $('#update_loading_indicator').show()
}

function resize_map() {
    var w = $(window).width() - $('#side').outerWidth() - 110;
    $('#map').width(w - 1);
    $('#explanation').width(w - 1);
    
    $('.olControlZoomPanel').css('top', $('#map').height() - $('.olControlZoomPanel').height() - 20);
    $('.olControlZoomPanel').css('left', $('#map').width() - $('.olControlZoomPanel').width() - 10);
    map.olMap.zoomToMaxExtent();
}

// Do these things even if the DOM isn't completely loaded

$('#map').hide();
$(window).load(function() {
    $('#map').show();
    resize_map();
});
$(window).resize(function() {
    resize_map();
});

$(document).ready(function() {
    $('#explanation').tabs();

    map = $('#map').gardenmap().data('gardenmap');

    $('#map_buttons').mapbuttons({
        jqmap: $('#map'),
    });

    submit_query();
    resize_map();

    $('#update_map').button();
    $('#update_map').click(function() {
        submit_query();
    });

    $('.borough').change(function() {
        var selected_borough = $(this).find(' :selected');
        if (selected_borough.attr('class') == "all") {
            $('.neighborhood:visible option').removeAttr('disabled');
        }
        else {
            var borough = selected_borough.val();

            // only show 'all' and this borough
            // TODO actually remove neighborhoods that aren't in this borough
            $('.neighborhood:visible option').attr('disabled', 'disabled');
            $('.neighborhood:visible option.all').removeAttr('disabled');
            $('.neighborhood:visible .' + borough).removeAttr('disabled');

            // if we were looking at a neighborhood outside of the new borough, fall back to 'all'
            if (borough != $('.neighborhood:visible option:selected').attr('class')) {
                $('.neighborhood:visible option.all').attr('selected', true);
            }
        }

    });
    
    $('.show_details').click(function() {
        var details = $(this).parents('li').find('.details');
        // position
        details.css('top', $(this).position().top);
        details.css('left', $(this).position().left + $(this).outerWidth() + 5);

        if (details.is(':hidden')) {
            // make sure we don't show more than one detail at a time
            $('#stats .details').hide();
            $('#stats .show_details').text('?');

            details.show();
            $(this).text('hide');
        }
        else {
            details.hide();
            $(this).text('?');
        }
    });

    $(':input.borough').change(function() {
        var v = $(this).val();
        sync_hidden_selects('borough', v);
    });

    $(':input.neighborhood').change(function() {
        var v = $(this).val();
        sync_hidden_selects('neighborhood', v);
    });

    $(':input.vegetables').change(function() {
        var v = $(this).val();
        sync_hidden_selects('vegetables', v);
    });

    $('#year').change(function(e) {
        var year_picked = $(this).val();
        map.changeGardensLayer(year_picked);
        $('#picker :input.year-dependent').hide();
        $('#picker :input.year-dependent.' + year_picked).show();
        submit_query();
    });
});
