from .models import UserProfile


def get_profile(user):
    # TODO make manager method
    return UserProfile.objects.get_or_create(user=user)[0]
