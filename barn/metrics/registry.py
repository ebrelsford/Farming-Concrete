"""
Tools to maintain a registry of metrics.

It looks like this:

- in ``yourapp/models.py``, register your metrics with ``metrics.register()``,

MetricRegistry
    Subclass of Python's dict type with registration/unregistration methods.

registry
    Instance of MetricRegistry.

register
    Proxy registry.register.
"""
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter


__all__ = ('MetricRegistry', 'registry', 'register',)


class MetricRegistry(dict):
    """
    Dict with some shortcuts to handle a registry of metrics.
    """

    def unregister(self, name):
        """Unregister a metric."""
        try:
            del self[name]
        except Exception:
            pass

    def register(self, metric_name, metric_details):
        """Register a metric."""
        metric_details['name'] = metric_name
        if 'app' not in metric_details:
            metric_details['app'] = metric_details['model']._meta.app_label
        if 'group' not in metric_details:
            metric_details['group'] = None
        self[metric_name] = metric_details

    def sorted(self, metrics=None):
        chosen_metrics = self.values()
        if metrics:
            chosen_metrics = [m for m in chosen_metrics if m['name'] in metrics]
        return sorted(chosen_metrics, key=itemgetter('group_number', 'number', 'name'))

    def by_group(self, metrics=None):
        grouped = groupby(self.sorted(metrics=metrics), lambda m: m['group'])
        g = OrderedDict()
        for group, metrics in grouped:
            g[group] = list(metrics)
        return g

    def get_for_model(self, model):
        for registered_metric in self.values():
            if registered_metric['model'] == model:
                return registered_metric
        return None


registry = MetricRegistry()


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)
