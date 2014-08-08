from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from feedback.models import Feedback
from registration.signals import user_activated
from templated_emails.utils import send_templated_email

from farmingconcrete.models import GardenType
from metrics.harvestcount.models import Gardener


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    # Gardens this user has access to. If none, and has 'any' permissions,
    # user can access all.
    gardens = models.ManyToManyField('farmingconcrete.Garden',
        blank=True,
        null=True,
        through='GardenMembership',
    )

    # GardenTypes this user is restricted to. If none, user can access all.
    garden_types = models.ManyToManyField(GardenType, blank=True, null=True)

    # The corresponding Gardener for this user, if any.
    gardener = models.ForeignKey(Gardener, blank=True, null=True)

    invite_count = models.PositiveIntegerField(default=0)


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
