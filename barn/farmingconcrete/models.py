from django.db import models
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditedModel


class GardenType(models.Model):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=32)


class Garden(models.Model):
    name = models.CharField('garden name', max_length=512)
    type = models.ForeignKey(GardenType)
    gardenid = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField('address', max_length=64)
    city = models.CharField(_('city'), max_length=128, null=True,
                            blank=True)
    state = models.CharField(_('state'), max_length=128, null=True,
                             blank=True)

    BOROUGH_CHOICES = (
        ('Brooklyn', 'Brooklyn'),
        ('Bronx', 'Bronx'),
        ('Manhattan', 'Manhattan'),
        ('Queens', 'Queens'),
        ('Staten Island', 'Staten Island'),
    )
    borough = models.CharField(max_length=32, choices=BOROUGH_CHOICES,
                               null=True, blank=True)
    neighborhood = models.CharField(max_length=64, null=True, blank=True)
    zip = models.CharField(max_length=16, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('can_edit_any_garden', 'Can edit any garden'),
        )

    def __unicode__(self):
        return self.name

    @staticmethod
    def counted():
        return Garden.objects.exclude(box=None)

    @staticmethod
    def uncounted():
        return Garden.objects.filter(box=None)


class GardenGroup(models.Model):
    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True, null=True)
    gardens = models.ManyToManyField('Garden', through='GardenGroupMembership')

    added_by = models.ForeignKey('auth.User')
    added = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.name


class GardenGroupMembership(models.Model):
    garden = models.ForeignKey('Garden')
    group = models.ForeignKey('GardenGroup')

    added_by = models.ForeignKey('auth.User', editable=False)
    added = models.DateTimeField(auto_now_add=True, editable=False)


# TODO delete
class Variety(AuditedModel):
    name = models.CharField(max_length=64)
    needs_moderation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Varieties'
        ordering = ['name']
        permissions = (
            ('add_variety_unmoderated', 'Can add varieties without moderation'),
        )

    def __unicode__(self):
        return self.name
