from .models import UserProfile


def get_profile(user):
    return UserProfile.objects.get_or_create(user=user)[0]
