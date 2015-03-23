from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GardenGroup


@receiver(post_save, sender=GardenGroup, dispatch_uid='farmingconcrete_gardengroup_add_admin')
def subscribe_organizer(sender, created=False, instance=None, **kwargs):
    if created:
        instance.add_admin(instance.added_by)
