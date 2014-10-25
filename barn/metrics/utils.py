import itertools

from django.contrib.auth.models import User
from django.db.models import Min

from farmingconcrete.models import Garden
from .registry import registry


def get_min_recorded(garden):
    metric_models = [m['model'] for m in registry.values()]
    min_dates = [m.objects.for_garden(garden).aggregate(min_date=Min('recorded'))['min_date'] for
                 m in metric_models]
    try:
        return min(filter(None, min_dates))
    except ValueError:
        return None


def get_gardens_with_records(start, end):
    metric_models = [m['model'] for m in registry.values()]
    gardens = [m.objects.for_dates(start, end).garden_pks() for m in metric_models]
    gardens = list(set(itertools.chain.from_iterable(gardens)))
    return Garden.objects.filter(pk__in=gardens).distinct()


def get_added_by(start, end, garden):
    metric_models = [m['model'] for m in registry.values()]
    users = [m.objects.for_dates(start, end).for_garden(garden).added_by_pks() for m in metric_models]
    users = list(set(itertools.chain.from_iterable(users)))
    return User.objects.filter(pk__in=users).distinct()
