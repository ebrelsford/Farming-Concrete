from django.apps import AppConfig

from actstream import registry


class FarmingConcreteAppConfig(AppConfig):
    name = 'farmingconcrete'

    def ready(self):
        from .signals import *
        registry.register(self.get_model('Garden'))
