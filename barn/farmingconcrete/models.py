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

    added_by = models.ForeignKey('auth.User', null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    has_metric_records = models.BooleanField(default=False)
    metric_records_count = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = (
            ('can_edit_any_garden', 'Can edit any garden'),
        )

    def __unicode__(self):
        return self.name

    def admins(self):
        """Get the admin users for this garden"""
        admins = self.gardenmembership_set.filter(
            is_admin=True,
        )
        return [a.user_profile.user for a in admins]

    def groups(self):
        """Get the groups this garden is actively a member of"""
        groups = GardenGroupMembership.objects.filter(garden=self) \
                .values_list('group__pk', flat=True)
        return GardenGroup.objects.filter(pk__in=groups)

    def groups_pending_requested(self):
        """Get the groups this garden has requested membership in"""
        groups = GardenGroupMembership.by_status.pending_requested() \
                .filter(garden=self).values_list('group__pk', flat=True)
        return GardenGroup.objects.filter(pk__in=groups).order_by('name')

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
        return reverse('farmingconcrete_gardens_user')


class GardenGroup(models.Model):
    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True, null=True)
    gardens = models.ManyToManyField('Garden', through='GardenGroupMembership')

    is_open = models.BooleanField(_('is open'),
        default=False,
        help_text=_('Can any garden join the group, or are they required to '
                    'get permission first?')
    )

    added_by = models.ForeignKey('auth.User')
    added = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def active_gardens(self):
        """Get the gardens this group actively contains"""
        gardens = GardenGroupMembership.objects.filter(group=self) \
                .values_list('garden__pk', flat=True)
        return Garden.objects.filter(pk__in=gardens).order_by('name')

    def requesting_gardens(self):
        """Get the gardens that have requested access to this group"""
        gardens = GardenGroupMembership.by_status.pending_requested() \
                .filter(group=self) \
                .values_list('garden__pk', flat=True)
        return Garden.objects.filter(pk__in=gardens).order_by('name')

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

    def admins(self):
        from accounts.models import GardenGroupUserMembership

        admin_members = GardenGroupUserMembership.objects.filter(
            is_admin=True,
            group=self,
        )
        return [a.user_profile.user for a in admin_members]

    def get_absolute_url(self):
        return reverse('farmingconcrete_gardengroup_detail', kwargs={ 'pk': self.pk })

    def members(self):
        from accounts.models import GardenGroupUserMembership

        return GardenGroupUserMembership.objects.filter(group=self)

    def is_admin(self, user):
        """Is the user an admin of this group?"""
        from accounts.models import GardenGroupUserMembership

        return GardenGroupUserMembership.objects.filter(
            is_admin=True,
            user_profile__user=user,
            group=self,
        ).exists()

    def is_admin_of_member_garden(self, user):
        """Is the user an admin of a garden in this group?"""
        from accounts.models import GardenMembership

        return GardenMembership.objects.filter(
            garden__in=self.active_gardens(),
            is_admin=True,
            user_profile__user=user,
        ).exists()

    def is_member_of_member_garden(self, user):
        """Is the user a member of a garden in this group?"""
        from accounts.models import GardenMembership

        return GardenMembership.objects.filter(
            garden__in=self.active_gardens(),
            user_profile__user=user,
        ).exists()

    def can_join(self, garden=None, user=None):
        # Open to anyone
        if self.is_open:
            return True

        # Already in it
        if garden and garden in self.active_gardens():
            return True

        # User is an admin (of group or site)
        if user and (self.is_admin(user) or user.has_perm('can_edit_any_garden')):
            return True
        return False

    def __unicode__(self):
        return self.name


class GardenGroupMembershipManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(GardenGroupMembershipManager, self).get_queryset().filter(
            status=GardenGroupMembership.ACTIVE
        )


class GardenGroupMembershipStatusQuerySet(models.QuerySet):

    def any(self):
        return self.all()

    def status_is(self, status):
        return self.filter(status=status)

    def active(self):
        return self.status_is(GardenGroupMembership.ACTIVE)

    def pending_invited(self):
        return self.status_is(GardenGroupMembership.PENDING_INVITED)

    def pending_requested(self):
        return self.status_is(GardenGroupMembership.PENDING_REQUESTED)


class GardenGroupMembership(models.Model):
    objects = GardenGroupMembershipManager()
    by_status = GardenGroupMembershipStatusQuerySet.as_manager()

    garden = models.ForeignKey('Garden')
    group = models.ForeignKey('GardenGroup')

    added_by = models.ForeignKey('auth.User', editable=False)
    added = models.DateTimeField(auto_now_add=True, editable=False)

    ACTIVE = 'active'
    PENDING_REQUESTED = 'pending_requested'
    PENDING_INVITED = 'pending_invited'
    STATUS_CHOICES = (
        (ACTIVE, 'active'),
        (PENDING_REQUESTED, 'pending: requested'),
        (PENDING_INVITED, 'pending: invited'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=ACTIVE)
