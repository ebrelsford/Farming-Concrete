from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class EmailOrUsernameModelBackend(object):
    """
    Allow users to log in with either their username or their email address.

    Adapted from
        https://djangosnippets.org/snippets/1001/
    """

    def authenticate(self, username=None, password=None):
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
            except User.MultipleObjectsReturned:
                raise PermissionDenied('Too many users with that email address!')
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
