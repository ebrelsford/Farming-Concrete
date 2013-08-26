from metrics.registry import registry


def metrics(request):
    """Add metrics to the context."""
    if 'djangojs' in request.path:
        return {}
    else:
        return {
            'grouped_metrics': registry.by_group(),
            'registered_metrics': registry,
        }
