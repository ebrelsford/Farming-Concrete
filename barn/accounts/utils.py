from .models import GardenMembership, UserProfile


def is_admin(user, garden):
    if user.has_perm('farmingconcrete.can_edit_any_garden'):
        return True
    return GardenMembership.objects.filter(
        garden=garden,
        is_admin=True,
        user_profile__user=user,
    ).exists()


def is_member(user, garden):
    if user.has_perm('farmingconcrete.can_edit_any_garden'):
        return True
    return GardenMembership.objects.filter(
        garden=garden,
        user_profile__user=user,
    ).exists()


def get_profile(user):
    # TODO make manager method
    return UserProfile.objects.get_or_create(user=user)[0]
