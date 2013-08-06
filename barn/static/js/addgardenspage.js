//
// addgardenspage
//
// Scripts for the add gardens page.
//

define(
    [
        'jquery',
        'django'
    ], function ($, Django) {

        function updateSuggestions() {
            var baseUrl = Django.url('farmingconcrete_gardens_suggest'),
                name = $('#id_name').val();
            $('.suggestions-wrapper').load(baseUrl + '?name=' + name);
        }

        $(document).ready(function () {
            $('#id_name').keyup(updateSuggestions);
        });

    }

);
