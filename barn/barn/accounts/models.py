from django.db import models
from django.contrib.auth.models import User

from farmingconcrete.models import Garden
from harvestcount.models import Gardener

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    gardens = models.ManyToManyField(Garden)
    gardener = models.ForeignKey(Gardener, unique=True)
