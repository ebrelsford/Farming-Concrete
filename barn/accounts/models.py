from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver

from registration.signals import user_activated

from farmingconcrete.models import GardenType
from metrics.harvestcount.models import Gardener


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    # Gardens this user has access to. If none, and has 'any' permissions,
    # user can access all.
    gardens = models.ManyToManyField('farmingconcrete.Garden',
        blank=True,
        null=True,
        through='GardenMembership',
    )

    # GardenTypes this user is restricted to. If none, user can access all.
    garden_types = models.ManyToManyField(GardenType, blank=True, null=True)

    # The corresponding Gardener for this user, if any.
    gardener = models.ForeignKey(Gardener, blank=True, null=True)


class GardenMembership(models.Model):
    garden = models.ForeignKey('farmingconcrete.Garden')
    user_profile = models.ForeignKey('UserProfile')
    is_admin = models.BooleanField(default=False)

    EMAIL_PREFERENCES_CHOICES = (
        ('all', 'all'),
        ('none', 'none'),
    )
    email_preferences = models.CharField(
        max_length=50,
        choices=EMAIL_PREFERENCES_CHOICES,
        default='all',
    )

    added_by = models.ForeignKey('auth.User', editable=False, null=True)
    added = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(user_activated)
def add_user_to_default_groups(sender, user, request, **kwargs):
    try:
        default_group_names = settings.DEFAULT_GROUPS
        default_groups = Group.objects.filter(name__in=default_group_names)
        user.groups.add(*default_groups)
        user.save()
    except Exception:
        pass
