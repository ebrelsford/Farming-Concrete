define(['jquery'], function ($) {
    /*
     * Get or create a plant type.
     * 
     * XXX Currently assumes you're on a page with an autocomplete plant type field.
     */
    function get_or_create_plant_type(url, name, force, callback) {
        if (name !== '') {
            // send new plant type to server
            $.post(url,
                {
                    'name': name,
                    'force': force ? 'true' : 'false',
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                },
                function (data) {
                    if (data.success) {
                        // update variety input
                        $('input[name="variety_text"]').val(data.name);
                        $('input[name="variety"]').val(data.id);

                        // post a message
                        $('#add-new-plant-type .message').text(data.message);

                        // hide add-new-plant-type form
                        $('input[name="new-plant-type"]').val('');
                        $('#add-new-plant-type .adder').hide();
                    }
                    else {
                        // post a message, with a link to try again / force
                        $('#add-new-plant-type .message').html(
                            'couldn\'t find "' + name + '" add it? ' +
                            '<a href="#">yes, please!</a>'
                        ).find('a').click(function () {
                            // force it this time
                            get_or_create_plant_type(url, name, true, callback);
                        });
                    }
                    callback(data);
                },
                'json'
            );

            return false;
        }
    }

    $(document).ready(function () {
        /*
         * Don't let <enter> in the variety autocomplete submit the form.
         */
        $(':input#id_variety_text,:input#id_gardener_text').keypress(function (e) {
            if (e.which === 13) {
                e.preventDefault();
            }
        });
        
    });

    return {
        get_or_create_plant_type: get_or_create_plant_type,
    };
});
