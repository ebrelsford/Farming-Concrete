//
// gardendetailpage
//

define(['jquery', 'django'], function ($, Django) {

    $(document).ready(function () {

        $('.btn-add-data-empty').click(function () {
            var confirm = window.confirm("You can't add data without joining a garden. Join one now?");
            if (confirm) {
                window.location.href = Django.url('farmingconcrete_gardens_add');
            }
            return false;
        });

    });

});
