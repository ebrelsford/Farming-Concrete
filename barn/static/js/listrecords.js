//
// listrecords
//

$(document).ready(function () {
    if ($('.record-list-page').length > 0) {
        $('.list-records-year').change(function () {
            window.location.href = $(this).find(':selected').val();
        });
    }
});
