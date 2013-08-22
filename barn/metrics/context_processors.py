from metrics.registry import registry


def metrics(request):
    """Add metrics to the context."""
    if 'djangojs' in request.path:
        return {}
    else:
        return {
            'registered_metrics': registry,
        }
