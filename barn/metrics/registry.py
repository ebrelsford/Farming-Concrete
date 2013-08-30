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
        if 'group' not in metric_details:
            metric_details['group'] = None
        self[metric_name] = metric_details

    def by_group(self):
        sorted_metrics = sorted(self.values(), key=itemgetter('group', 'name'))
        grouped = groupby(sorted_metrics, lambda m: m['group'])
        g = {}
        for group, metrics in grouped:
            g[group] = list(metrics)
        return g


registry = MetricRegistry()


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)
