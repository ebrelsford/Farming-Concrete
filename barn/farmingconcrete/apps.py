from django.apps import AppConfig


class FarmingConcreteAppConfig(AppConfig):
    name = 'farmingconcrete'

    def ready(self):
        from .signals import *
        from actstream import registry
        registry.register(self.get_model('Garden'))
        registry.register(self.get_model('GardenGroup'))
