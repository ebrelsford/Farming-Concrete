define(
    [
        'jquery',
    ], function ($) {
        var geocoder = new google.maps.Geocoder();

        function geocode(address, state, f) {
            state = state.toUpperCase();
            geocoder.geocode({
                'address': address
            }, function (results, status) {
                for (var i = 0; i < results.length; i++) {
                    var result_state = get_component(results[i],
                                                     'administrative_area_level_1');
                    if (result_state.short_name === state ||
                        result_state.long_name === state) {
                        return f(results[i], status);
                    }
                }
                return f(null, status);
            });
        }

        function get(result, component) {
            return get_component(result, component).short_name;
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
            'get_city': get_city,
            'get_state': get_state,
            'get_zip': get_zip,
            'get_longitude': get_longitude,
            'get_latitude': get_latitude
        };
    }
);
