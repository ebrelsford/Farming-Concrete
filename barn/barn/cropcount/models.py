from django.db import models

from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import Garden, Variety
    
class Box(models.Model):
    class Meta:
        verbose_name_plural = 'Boxes'
        ordering = ['name']

    garden = models.ForeignKey(Garden)
    name = models.CharField(
        max_length=32
    )
    length = models.DecimalField(max_digits=4, decimal_places=1)
    width = models.DecimalField(max_digits=4, decimal_places=1)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s), %d x %d" % (self.garden.name, self.name, self.length, self.width)

class Patch(models.Model):
    class Meta:
        verbose_name_plural = 'Patches'
        ordering = ['variety']

    box = models.ForeignKey(Box)
    variety = models.ForeignKey(Variety)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        area = self.area
        if not area:
            area = 0
        return "%s (%s), %s: %d (plants), %d (area)" % (self.box.garden.name, self.box.name, self.variety, self.plants, area)
