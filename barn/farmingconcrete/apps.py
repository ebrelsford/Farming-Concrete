from django.apps import AppConfig


class FarmingConcreteAppConfig(AppConfig):
    name = 'farmingconcrete'

    def ready(self):
        from .signals import *
