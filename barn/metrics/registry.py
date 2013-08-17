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
        self[metric_name] = metric_details


registry = MetricRegistry()


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)
