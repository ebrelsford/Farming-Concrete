from django.db import models

from audit.models import AuditedModel
from farmingconcrete.models import Garden
from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class CropCountQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'crop__name',
            'crop_variety__name',
            'quantity',
        )
        record_dicts = self.values(*values_args)

        # Rename 'quantity' to 'plants'
        for record_dict in record_dicts:
            record_dict['plants'] = record_dict['quantity']
            del record_dict['quantity']

        return record_dicts


class CropCountManager(MetricManager):
    
    def get_queryset(self):
        return CropCountQuerySet(self.model)


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


class Patch(BaseMetricRecord):
    class Meta:
        verbose_name_plural = 'Patches'
        ordering = ['crop']

    objects = CropCountManager()

    box = models.ForeignKey(Box)

    crop = models.ForeignKey('crops.Crop', null=True)
    crop_variety = models.ForeignKey('crops.Variety', blank=True, null=True)

    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    UNITS_CHOICES = (
        ('plants', 'plants'),
        ('row feet', 'row feet'),
        ('square feet', 'square feet'),
    )
    units = models.CharField(max_length=15, choices=UNITS_CHOICES)

    def __unicode__(self):
        return "%.1f %s of %s" % (
            self.quantity or 0,
            self.units,
            self.crop,
        )

    def get_bed_display(self):
        if self.box:
            return self.box.name
        return None

    def _bed_width(self):
        if self.box and self.box.width:
            return self.box.width
        return None
    bed_width = property(_bed_width)

    def _bed_length(self):
        if self.box and self.box.length:
            return self.box.length
        return None
    bed_length = property(_bed_length)

    def get_crop_variety_display(self):
        if self.crop_variety:
            return self.crop_variety.name
        return None

    @classmethod
    def summarize(cls, patches):
        if not patches:
            return None
        box_pks = set(patches.values_list('box__pk', flat=True))
        beds = Box.objects.filter(pk__in=box_pks)
        return {
            'count': patches.count(),
            'beds': beds.count(),
            'area': beds.extra(select = {'area': 'SUM(length * width)'})[0].area,
            'plants': patches.filter(units='plants').aggregate(models.Sum('quantity'))['quantity__sum'],
            'recorded_max': patches.aggregate(models.Max('recorded'))['recorded__max'],
        }
