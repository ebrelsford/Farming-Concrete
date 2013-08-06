from django.db import models
from django.contrib.auth.models import User

from farmingconcrete.models import Garden, GardenType
from harvestcount.models import Gardener


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # Gardens this user has access to. If none, and has 'any' permissions, user can access all.
    gardens = models.ManyToManyField(Garden, blank=True, null=True)

    # GardenTypes this user is restricted to. If none, user can access all.
    garden_types = models.ManyToManyField(GardenType, blank=True, null=True)

    # The corresponding Gardener for this user, if any.
    gardener = models.ForeignKey(Gardener, blank=True, null=True)
