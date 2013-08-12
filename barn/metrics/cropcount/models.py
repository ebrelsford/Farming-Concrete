from django.db import models

from audit.models import AuditedModel
from farmingconcrete.models import Garden, Variety


class Box(AuditedModel):
    class Meta:
        verbose_name_plural = 'Boxes'
        ordering = ['name']

    garden = models.ForeignKey(Garden)
    name = models.CharField(
        max_length=32
    )
    length = models.DecimalField(max_digits=4, decimal_places=1)
    width = models.DecimalField(max_digits=4, decimal_places=1)

    def __unicode__(self):
        return "%s (%s), %d x %d" % (self.garden.name, self.name, self.length,
                                     self.width)

    def __cmp__(self, other):
        """sort naturally, with numbers in numeric order"""
        if self.name.isdigit():
            if other.name.isdigit():
                return cmp(int(self.name), int(other.name))
            else:
                return -1
        else:
            if other.name.isdigit():
                return 1
            else:
                return cmp(self.name, other.name)


class Patch(AuditedModel):
    class Meta:
        verbose_name_plural = 'Patches'
        ordering = ['variety']

    box = models.ForeignKey(Box)
    variety = models.ForeignKey(Variety)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                               blank=True)

    estimated_plants = models.BooleanField(
        default=False,
        help_text=('True if the number of plants in this patch was estimated '
                   'using average plants per square foot.')
    )

    def __unicode__(self):
        return "%s (%s), %s: %d (plants), %d (area)" % (
            self.box.garden.name,
            self.box.name,
            self.variety,
            self.plants or 0,
            self.area or 0,
        )
