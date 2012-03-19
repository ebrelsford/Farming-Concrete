from datetime import date

from django.db.models import Sum

from chart_builders import create_chart_as_png_str
from cropcount.models import Patch
from harvestcount.models import Harvest
from estimates.common import estimate_for_patches

# TODO parameterize
REPORT_START = date(2011, 01, 01)
REPORT_END = date(2012, 01, 01)

def _harvests(garden, start=REPORT_START, end=REPORT_END):
    """Get valid harvests for the given garden"""
    return Harvest.objects.filter(gardener__garden=garden, harvested__gte=start, harvested__lt=end)

def _patches(garden, start=REPORT_START, end=REPORT_END):
    """Get valid patches for the given garden"""
    return Patch.objects.filter(box__garden=garden, added__gte=start, added__lt=end)

def plants_per_crop(garden, medium="screen"):
    patches = _patches(garden).exclude(plants=None)
    crops = patches.values('variety__name').annotate(plants=Sum('plants'))

    data = {
        'data': [[c['plants'] for c in crops]],
    }
    labels = {
        'x': '',
        'y': 'number of plants',
        'title': '',
    }

    return create_chart_as_png_str('barchart', data, labels, '', xlabels=[c['variety__name'] for c in crops], medium=medium)

def weight_per_crop(garden, medium="screen"):
    harvests = _harvests(garden).exclude(weight=None)
    harvest_totals = harvests.values('variety__name').annotate(weight=Sum('weight')).order_by('variety__name')

    data = {
        'data': [[h['weight'] for h in harvest_totals]],
    }
    labels = {
        'x': '',
        'y': 'total weight measured (lbs)',
        'title': '',
    }

    return create_chart_as_png_str('barchart', data, labels, '', xlabels=[h['variety__name'] for h in harvest_totals], medium=medium)

def weight_per_gardener(garden, medium="screen"):
    harvests = _harvests(garden).exclude(weight=None)
    gardener_totals = harvests.values('gardener__name').annotate(weight=Sum('weight')).order_by('gardener__name')

    data = {
        'data': [[g['weight'] for g in gardener_totals]],
    }
    labels = {
        'x': '',
        'y': 'total weight measured (lbs)',
        'title': '',
    }

    return create_chart_as_png_str('barchart', data, labels, '', xlabels=[g['gardener__name'] for g in gardener_totals], medium=medium)

def estimated_weight_per_crop(garden, medium="screen"):
    patches = _patches(garden).exclude(plants=None)
    estimated_yields = estimate_for_patches(patches, estimate_yield=True)['crops']

    print estimated_yields

    data = {
        'data': [[y['estimated_yield'] or 0 for y in estimated_yields]],
    }
    labels = {
        'x': '',
        'y': 'estimated yield (lbs)',
        'title': '',
    }

    return create_chart_as_png_str('barchart', data, labels, '', xlabels=[y['variety__name'] for y in estimated_yields], medium=medium)
