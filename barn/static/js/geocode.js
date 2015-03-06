define(
    [
        'jquery',
    ], function ($) {
        var geocoder = new google.maps.Geocoder();

        function geocode(address, state, f) {
            state = state.toLowerCase();
            geocoder.geocode({
                'address': address
            }, function (results, status) {
                if (state) {
                    for (var i = 0; i < results.length; i++) {
                        var result_state = get_component(results[i],
                                                         'administrative_area_level_1');
                        if (result_state && (result_state.short_name.toLowerCase() === state ||
                            result_state.long_name.toLowerCase() === state)) {
                            return f(results[i], status);
                        }
                    }
                }
                else {
                    // If no state to compare to, just pick the best match
                    return f(results[0], status);
                }
                return f(null, status);
            });
        }

        function get(result, desired_type) {
            var component = get_component(result, desired_type);
            if (component) {
                return component.short_name;
            }
            else {
                return null;
            }
        }

        function get_component(result, desired_type) {
            var matches = $.grep(result.address_components, function (component, i) {
                return ($.inArray(desired_type, component.types) >= 0);
            });
            if (matches.length >= 0 && matches[0] !== null) {
                return matches[0];
            }
            return null;
        }

        function get_street(result) {
            var street_number = get(result, 'street_number');
            var route = get(result, 'route');
            if (street_number === null || route === null) {
                return null;
            }
            return street_number + ' ' + route;
        }

        function get_neighborhood(result) {
            return get(result, 'neighborhood');
        }

        function get_borough(result) {
            return get(result, 'sublocality');
        }

        function get_city(result) {
            var city = get(result, 'sublocality');
            if (city === null) {
                city = get(result, 'locality');
            }
            return city;
        }

        function get_state(result) {
            return get(result, 'administrative_area_level_1');
        }

        function get_country(result) {
            return get(result, 'country');
        }

        function get_zip(result) {
            return get(result, 'postal_code');
        }

        function get_longitude(result) {
            return result.geometry.location.lng();
        }

        function get_latitude(result) {
            return result.geometry.location.lat();
        }

        return {
            'geocode': geocode,
            'get': get,
            'get_street': get_street,
            'get_neighborhood': get_neighborhood,
            'get_borough': get_borough,
            'get_city': get_city,
            'get_state': get_state,
            'get_country': get_country,
            'get_zip': get_zip,
            'get_longitude': get_longitude,
            'get_latitude': get_latitude
        };
    }
);
