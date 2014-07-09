//
// gardenmemberlist
//

define(['jquery', 'django'], function ($, Django) {

    $(document).ready(function () {

        $('.add-admin').click(function () {
            var confirm = window.confirm('Add user as admin? They will receive emails about this garden and be able to add and remove other admins.');
            if (!confirm) return;

            var url = Django.url('gardenmemberships_admin_add', { 'pk': $(this).data('membershipPk' )});
            $.get(url)
                .then(function () {
                    location.reload(true);
                })
                .fail(function () {
                    alert('There was an error while trying to add this user as admin. Try again and use the feedback button to let us know if it persists. Sorry about that!');
                });
            return false;
        });

        $('.delete-admin').click(function () {
            var confirm = window.confirm('Remove user as admin? They will no longer receive emails about this garden or be able to add and remove other admins.');
            if (!confirm) return;

            var url = Django.url('gardenmemberships_admin_delete', { 'pk': $(this).data('membershipPk' )});
            $.get(url)
                .then(function () {
                    location.reload(true);
                })
                .fail(function () {
                    alert('There was an error while trying to remove this user as admin. Try again and use the feedback button to let us know if it persists. Sorry about that!');
                });
            return false;
        });

        $('.delete-member').click(function () {
            var confirm = window.confirm('Remove user? They will no longer be able to add data to the garden.');
            if (!confirm) return;

            var url = Django.url('gardenmemberships_member_delete', {
                pk: $(this).data('membershipPk')
            });
            $.get(url)
                .then(function () {
                    location.reload(true);
                })
                .fail(function () {
                    alert('There was an error while trying to remove this user. Try again and use the feedback button to let us know if it persists. Sorry about that!');
                });
            return false;
        });

    });

});
