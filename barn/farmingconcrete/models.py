from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GardenType(models.Model):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)


class PrivacyMixin(models.Model):
    share_name = models.BooleanField(_('share garden name'),
        default=False,
        help_text=_("Share the garden's name in publicly available data."),
    )
    share_location = models.BooleanField(_('share garden location'),
        default=False,
        help_text=_("Share the garden's location in publicly available data."),
    )

    class Meta:
        abstract = True


class Garden(PrivacyMixin, models.Model):
    name = models.CharField('garden name', max_length=512)
    type = models.ForeignKey(GardenType)
    gardenid = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField('address', max_length=64)
    city = models.CharField(_('city'), max_length=128, null=True,
                            blank=True)
    state = models.CharField(_('state'), max_length=128, null=True,
                             blank=True)
    country = models.CharField(_('country'), max_length=128, null=True,
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
    zip = models.CharField(_('postal code'), max_length=16, null=True,
                           blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    has_metric_records = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('can_edit_any_garden', 'Can edit any garden'),
        )

    def __unicode__(self):
        return self.name

    def is_admin(self, user):
        """Returns true if the given user is an admin of this garden"""
        if user.has_perm('farmingconcrete.can_edit_any_garden'):
            return True
        return self.gardenmembership_set.filter(
            is_admin=True,
            user_profile__user=user,
        ).exists()

    def is_member(self, user):
        """Returns true if the given user is a member of this garden"""
        if user.has_perm('farmingconcrete.can_edit_any_garden'):
            return True
        return self.gardenmembership_set.filter(
            user_profile__user=user,
        ).exists()

    def get_absolute_url(self):
        return reverse('farmingconcrete_garden_details', kwargs={ 'pk': self.pk })


class GardenGroup(models.Model):
    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True, null=True)
    gardens = models.ManyToManyField('Garden', through='GardenGroupMembership')

    added_by = models.ForeignKey('auth.User')
    added = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def add_admin(self, user):
        """Add the given user as an admin of this group."""
        from accounts.models import GardenGroupUserMembership
        from accounts.utils import get_profile

        membership, created = GardenGroupUserMembership.objects.get_or_create(
            group=self,
            user_profile=get_profile(user),
            defaults={ 'added_by': user, 'is_admin': True },
        )
        if not created:
            membership.is_admin = True
        membership.save()
        return membership

    def __unicode__(self):
        return self.name


class GardenGroupMembership(models.Model):
    garden = models.ForeignKey('Garden')
    group = models.ForeignKey('GardenGroup')

    added_by = models.ForeignKey('auth.User', editable=False)
    added = models.DateTimeField(auto_now_add=True, editable=False)
