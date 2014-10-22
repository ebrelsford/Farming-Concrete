from django.db.models import Min

from .registry import registry


def get_min_recorded(garden):
    metric_models = [m['model'] for m in registry.values()]
    min_dates = [m.objects.for_garden(garden).aggregate(min_date=Min('recorded'))['min_date'] for
                 m in metric_models]
    try:
        return min(filter(None, min_dates))
    except ValueError:
        return None
