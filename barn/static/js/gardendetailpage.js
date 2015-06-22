//
// gardendetailpage
//

var $ = require('jquery');
var Django = require('django');

$(document).ready(function () {
    if ($('.garden-detail-page').length > 0) {
        $('.btn-add-data-empty').click(function () {
            var confirm = window.confirm("You can't add data without joining a garden. Join one now?");
            if (confirm) {
                window.location.href = Django.url('farmingconcrete_gardens_add');
            }
            return false;
        });

        $('.year-picker-select').change(function () {
            var year = $(this).val(),
                url = Django.url('farmingconcrete_gardens_user');

            if (year) {
                url = Django.url('farmingconcrete_gardens_user_by_year', {
                    year: $(this).val()
                });
            }
            window.location.href = url;
        });
    }
});
