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
                name = $('#id_name').val(),
                url = baseUrl + '?name=' + name;
            $('.garden-suggestions-wrapper').load(url, activateSuggestedGardens);
        }

        function activateSuggestedGardens() {
            $('.garden-suggestion').click(function () {
                selectSuggestedGarden($(this).data('pk'));
            });
        }

        function selectSuggestedGarden(pk) {
            window.location.href = Django.url('farmingconcrete_gardens_suggest_add', { 'pk': pk });
        }

        $(document).ready(function () {
            $('#id_name').keyup(function () {
                if ($(this).val().length >= 5) {
                    updateSuggestions();
                }
            });
        });

    }

);
