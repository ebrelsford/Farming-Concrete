//
// recordlistpage
//

define(
    [
        // Requirements with exports
        'jquery',
        'django',
        'prefixurl'

    ], function ($, Django, prefixurl) {

        $(document).ready(function () {
            $('.record-list-page').on('click', '.delete-record', function () {
                var confirmed = confirm('Delete record? There is no undo and the data will be lost.');
                if (!confirmed) {
                    return;
                }
                var record = $(this).parents('.record');
                var delete_url = prefixurl.url('metrics_delete_record', {
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
        });

    }
);
