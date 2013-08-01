from django.db import models

from hashlib import sha1
from random import random

from farmingconcrete.models import Garden

class SharedReport(models.Model):
    garden = models.ForeignKey(Garden)
    valid_year = models.PositiveIntegerField()
    access_key = models.CharField(max_length=40, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.access_key = sha1(str(self.garden.id + random())).hexdigest()
        super(SharedReport, self).save(*args, **kwargs)

class Chart(models.Model):
    garden = models.ForeignKey(Garden)
    label = models.CharField(max_length=32)
    image = models.ImageField(upload_to='charts')
