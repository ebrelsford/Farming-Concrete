from django.db import models

from audit.models import AuditedModel
from farmingconcrete.models import Garden, Variety

class Gardener(AuditedModel):
    garden = models.ForeignKey(Garden)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class Harvest(AuditedModel):
    gardener = models.ForeignKey(Gardener)
    variety = models.ForeignKey(Variety)

    weight = models.DecimalField(max_digits=6, decimal_places=2)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    harvested = models.DateField()
    reportable = models.BooleanField(default=True)
