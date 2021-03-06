from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from feedback.models import Feedback
from registration.signals import user_activated
from templated_emails.utils import send_templated_email

from metrics.harvestcount.models import Gardener


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    # Gardens this user has access to. If none, and has 'any' permissions,
    # user can access all.
    gardens = models.ManyToManyField('farmingconcrete.Garden',
        blank=True,
        through='GardenMembership',
    )

    # GardenTypes this user is restricted to. If none, user can access all.
    garden_types = models.ManyToManyField('farmingconcrete.GardenType', blank=True)

    # The corresponding Gardener for this user, if any.
    gardener = models.ForeignKey(Gardener, blank=True, null=True)

    invite_count = models.PositiveIntegerField(default=0)
    email_address_public = models.BooleanField(default=False)


class GardenMembership(models.Model):
    garden = models.ForeignKey('farmingconcrete.Garden')
    user_profile = models.ForeignKey('UserProfile')
    is_admin = models.BooleanField(default=False)

    EMAIL_PREFERENCES_CHOICES = (
        ('all', 'all'),
        ('none', 'none'),
    )
    email_preferences = models.CharField(
        max_length=50,
        choices=EMAIL_PREFERENCES_CHOICES,
        default='all',
    )

    added_by = models.ForeignKey('auth.User', editable=False, null=True)
    added = models.DateTimeField(auto_now_add=True, editable=False)


class GardenGroupUserMembership(models.Model):
    """
    Represents the membership of a user in a garden group.
    
    Previously we assumed that the person who added a garden group was the 
    owner and admin of it, but this is too simplistic as there may be multiple
    admins of a group and the person who added the group may be a site
    administrator rather than a group admin.
    """
    group = models.ForeignKey('farmingconcrete.GardenGroup')
    user_profile = models.ForeignKey('UserProfile')
    is_admin = models.BooleanField(default=False)

    added_by = models.ForeignKey('auth.User', editable=False, null=True)
    added = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(post_save, sender=GardenMembership)
def new_garden_membership(sender, instance, created=False, **kwargs):
    if created:
        # Try to find admins for this garden that are not the new person
        admins = GardenMembership.objects.filter(
            garden=instance.garden,
            is_admin=True,
        ).exclude(user_profile=instance.user_profile)
        if admins:
            send_templated_email(
                [admin.user_profile.user.email for admin in admins],
                'emails/new_garden_membership',
                {
                    'base_url': settings.BASE_URL,
                    'garden': instance.garden,
                    'new_user': instance.user_profile.user,
                }
            )


@receiver(user_activated)
def add_user_to_default_groups(sender, user, request, **kwargs):
    try:
        default_group_names = settings.DEFAULT_GROUPS
        default_groups = Group.objects.filter(name__in=default_group_names)
        user.groups.add(*default_groups)
        user.save()
    except Exception:
        pass


@receiver(post_save, sender=Feedback)
def new_feedback(sender, instance, created=False, **kwargs):
    """Send email when new feedback is sent via the feedback button"""
    if created:
        send_templated_email(
            [email for name, email in settings.ADMINS],
            'emails/new_feedback',
            { 'feedback': instance, }
        )
