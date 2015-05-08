//
// recordlistpage
//

var $ = require('jquery');
var Django = require('django');

$(document).ready(function () {
    if ($('.record-list-page').length > 0) {
        $('.record-list-page').on('click', '.delete-record', function () {
            var confirmed = confirm('Delete record? There is no undo and the data will be lost.');
            if (!confirmed) {
                return;
            }
            var record = $(this).parents('.record').eq(0);
            var delete_url = Django.url('metrics_delete_record', {
                pk: record.data('pk'),
                record_type_pk: record.data('record-type-pk')
            });

            $.post(delete_url, { csrfmiddlewaretoken: Django.csrf_token() })
                .done(function () {
                    record.hide();
                })
                .fail(function () {
                    alert('Could not delete record. Let an administrator know if this continues to occur.');
                });

        });
    }
});
