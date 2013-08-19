from metrics.registry import registry


def metrics(request):
    """Add metrics to the context."""
    return {
        'registered_metrics': registry,
    }
