from django.db.models.signals import post_save
from django.dispatch import receiver

from .actions import new_garden_group_action
from .models import GardenGroup


@receiver(post_save, sender=GardenGroup, dispatch_uid='farmingconcrete_gardengroup_add_admin')
def subscribe_organizer(sender, created=False, instance=None, **kwargs):
    if created:
        instance.add_admin(instance.added_by)


@receiver(post_save, sender=GardenGroup,
          dispatch_uid='farmingconcrete_gardengroup_add_action')
def add_garden_group_action(sender, created=False, instance=None, **kwargs):
    if not (created and instance):
        return
    new_garden_group_action(instance, instance.added_by)
