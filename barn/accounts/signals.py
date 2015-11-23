from django.dispatch import receiver

from actstream import action
from registration.signals import user_activated


@receiver(user_activated)
def add_user_activated_action(sender, user, request, **kwargs):
    action.send(user, verb='joined Farming Concrete')
