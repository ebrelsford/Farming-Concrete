//
// listrecords
//

define(['jquery'], function ($) {

    $(document).ready(function () {
        $('.list-records-year').change(function () {
            window.location.href = $(this).find(':selected').val();
        });
    });

});
