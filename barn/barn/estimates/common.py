from datetime import date

from django.db.models import Sum

from models import EstimatedCost, EstimatedYield

def _find_estimated_crop_yield(variety_id, recorded_date):
    try:
        return EstimatedYield.objects.filter(variety__id=variety_id, valid_start__lte=recorded_date, valid_end__gt=recorded_date, should_be_used=True)[0].pounds_per_plant
    except:
        return None

def _estimate_yield(variety_id, recorded_date, plants):
    estimate = _find_estimated_crop_yield(variety_id, recorded_date)
    if estimate:
        return estimate.pounds_per_plant * plants
    return None

def estimate_for_harvests_by_gardener(harvests, estimate_value=False):
    rows = harvests.values('variety__id', 'gardener__name').annotate(pounds=Sum('weight')).distinct()
    total_value = 0
    gardener_values = {}
    for row in rows:
        gardener = row['gardener__name']
        gardener_values[gardener] = 0
        if estimate_value:
            row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(2011, 6, 1), row['pounds'])
            gardener_values[gardener] += estimated_value or 0
            total_value += estimated_value or 0

    return {
        'rows': rows,
        'total_value': total_value,
        'gardener_values': gardener_values,
    }

def estimate_for_harvests(harvests, estimate_value=False):
    rows = harvests.values('variety__id', 'variety__name').annotate(pounds=Sum('weight')).distinct()
    total_value = 0
    for row in rows:
        if estimate_value:
            row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(2011, 6, 1), row['pounds'])
            total_value += estimated_value

    return {
        'rows': rows,
        'total_value': total_value,
    }

def estimate_for_patches(patches, estimate_yield=False, estimate_value=False):
    """
    Estimate the pounds yielded by the given patches, including a total of all patches.
    """
    crops = patches.values('variety__id', 'variety__name').annotate(plants=Sum('plants'), area=Sum('area')).distinct()
    total_value = 0
    total_yield = 0
    for crop in crops:
        if estimate_yield:
            # XXX TODO should use 'added' to get more granular estimated yield
            crop['average_yield'] = _find_estimated_crop_yield(crop['variety__id'], date(2011, 6, 1))
            crop['estimated_yield'] = estimated_yield = (crop['average_yield'] or 0) * (crop['plants'] or 0)
            total_yield += estimated_yield or 0
        if estimate_value:
            crop['estimated_value'] = estimated_value = _estimate_value(crop['variety__id'], date(2011, 6, 1), crop['estimated_yield'])
            total_value += estimated_value or 0
    return {
        'crops': crops,
        'total_yield': total_yield,
        'total_value': total_value,
    }

def _estimate_value(variety_id, recorded_date, pounds):
    estimates = EstimatedCost.objects.filter(variety__id=variety_id, valid_start__lte=recorded_date, valid_end__gt=recorded_date, should_be_used=True)
    try:
        return estimates[0].cost_per_pound * pounds
    except:
        return None
