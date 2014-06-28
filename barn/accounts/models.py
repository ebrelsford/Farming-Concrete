from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from registration.signals import user_activated

from farmingconcrete.models import Garden, GardenType
from metrics.harvestcount.models import Gardener


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Gardens this user has access to. If none, and has 'any' permissions,
    # user can access all.
    gardens = models.ManyToManyField(Garden, blank=True, null=True)

    # GardenTypes this user is restricted to. If none, user can access all.
    garden_types = models.ManyToManyField(GardenType, blank=True, null=True)

    # The corresponding Gardener for this user, if any.
    gardener = models.ForeignKey(Gardener, blank=True, null=True)


@receiver(user_activated)
def add_user_to_default_groups(sender, user, request, **kwargs):
    try:
        default_group_names = settings.DEFAULT_GROUPS
        default_groups = Group.objects.filter(name__in=default_group_names)
        user.groups.add(*default_groups)
        user.save()
    except Exception:
        pass
