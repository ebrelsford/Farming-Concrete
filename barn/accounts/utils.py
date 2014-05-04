from .models import UserProfile


def get_profile(user):
    try:
        return user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        profile.save()
        return profile
