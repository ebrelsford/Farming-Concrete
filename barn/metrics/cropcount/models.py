from django.db import models

from audit.models import AuditedModel
from farmingconcrete.models import Garden, Variety
from ..models import BaseMetricRecord
from ..registry import register


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

    @classmethod
    def summarize(cls, patches):
        if not patches:
            return None
        box_pks = set(patches.values_list('box__pk', flat=True))
        beds = Box.objects.filter(pk__in=box_pks)
        return {
            'beds': beds.count(),
            'area': beds.extra(select = {'area': 'SUM(length * width)'})[0].area,
            'plants': patches.aggregate(models.Sum('plants'))['plants__sum'],
        }


register('Crop Count', {
    'all_gardens_url_name': 'cropcount_all_gardens',
    'model': Patch,
    'number': 1,
    'garden_detail_url_name': 'cropcount_garden_details',
    'group': 'Food Production',
    'group_number': 0,
    'index_url_name': 'cropcount_index',
    'user_gardens_url_name': 'cropcount_user_gardens',
})
