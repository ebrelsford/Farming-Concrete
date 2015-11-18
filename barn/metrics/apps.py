from django.apps import AppConfig

from actstream import registry


class MetricConfig(AppConfig):

    def ready(self):
        for model in self.get_metric_models():
            registry.register(model)
