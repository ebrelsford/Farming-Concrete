from django.apps import AppConfig


class MetricConfig(AppConfig):

    def ready(self):
        from actstream import registry

        for model in self.get_metric_models():
            registry.register(model)
