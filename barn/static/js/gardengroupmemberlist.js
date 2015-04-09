//
// gardengroupmemberlist
//

define(['jquery', 'django'], function ($, Django) {

    $(document).ready(function () {

        $('.delete-member').click(function () {
            var confirm = window.confirm("Remove user? They will no longer be able to access the group's data and add gardens to it.");
            if (!confirm) return;

            var url = Django.url('gardengroupmemberships_member_delete', {
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
