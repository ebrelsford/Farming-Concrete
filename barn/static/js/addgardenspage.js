//
// addgardenspage
//
// Scripts for the add gardens page.
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',

        // Other requirements
        'jquery.spin'
    ], function ($, Django) {

        function updateSuggestions() {
            var baseUrl = Django.url('farmingconcrete_gardens_suggest'),
                name = $('#id_name').val(),
                url = baseUrl + '?name=' + name,
                $wrapper = $('.garden-suggestions-wrapper');
            $wrapper
                .spin('large')
                .addClass('is-loading')
                .load(url, function () {
                    $wrapper
                        .spin(false)
                        .removeClass('is-loading');
                    activateSuggestedGardens();
                });
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
