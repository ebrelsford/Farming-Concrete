from datetime import date

from django.db.models import Min, Sum

from models import EstimatedCost, EstimatedYield

def _find_estimated_crop_yield(variety_id, year, garden_type=None):
    """
    Find the most recent valid EstimatedYield in the year given for the variety/garden type given.
    """
    try:
        yields = EstimatedYield.objects.filter(variety__id=variety_id, valid_start__year=year, should_be_used=True).order_by('-estimated')
        if garden_type:
            yields = yields.filter(garden_type=garden_type)
        return yields[0].pounds_per_plant
    except:
        return None

def _find_estimated_dollar_value(variety_id, year):
    try:
        estimates = EstimatedCost.objects.filter(variety__id=variety_id, valid_start__year=year, should_be_used=True).order_by('-estimated')
        return estimates[0].cost_per_pound
    except:
        return None

def estimate_for_harvests_by_gardener_and_variety(harvests):
    """Estimate value of harvests for the given harvests, grouped by gardener and variety"""
    gardener_variety_weights = harvests.values('variety__id', 'gardener__name').annotate(pounds=Sum('weight')).distinct()
    total_value = 0
    gardener_totals = {}

    for row in gardener_variety_weights:
        gardener = row['gardener__name']
        weight = row['pounds']
        gardener_totals[gardener] = dict(value=0, weight=0)

        row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(2011, 6, 1), weight) # TODO un-hard-code

        gardener_totals[gardener]['value'] += estimated_value or 0
        gardener_totals[gardener]['weight'] += weight or 0
        total_value += estimated_value or 0

    return {
        'gardener_variety_weights': gardener_variety_weights,
        'gardener_totals': gardener_totals,
        'total_value': total_value,
    }

def estimate_for_harvests(harvests, estimate_value=False):
    rows = harvests.values('variety__id', 'variety__name').annotate(pounds=Sum('weight')).distinct()
    total_value = 0
    for row in rows:
        if estimate_value:
            row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(2011, 6, 1), row['pounds']) # TODO un-hard-code
            total_value += estimated_value

    return {
        'rows': rows,
        'total_value': total_value,
    }

def estimate_for_patches(patches, estimate_yield=False, estimate_value=False, garden_type=None):
    """
    Estimate the pounds yielded by the given patches, including a total of all patches.
    """
    #
    # Try to get sum of plants/area by variety for the patches given.
    #
    # This is slightly complicated by our desire to make estimates valid only for certain dates.
    #
    crops = patches.values('variety__id', 'variety__name').annotate(plants=Sum('plants'), area=Sum('area'), min_added=Min('added')).distinct()
    total_value = 0
    total_value_by_garden_type = 0
    total_yield = 0
    total_yield_by_garden_type = 0

    for crop in crops:
        year = crop['min_added'].year # for now, only use year. could make this an option or use multiple functions.
        print year
        variety_id = crop['variety__id']

        # find average/estimate overall yield for the patches given containing this crop
        if estimate_yield:
            crop['average_yield'] = _find_estimated_crop_yield(variety_id, year)
            crop['estimated_yield'] = estimated_yield = (crop['average_yield'] or 0) * (crop['plants'] or 0)
            total_yield += estimated_yield or 0

            # if we have a garden type, get average/estimate for that type
            if garden_type:
                crop['type_average_yield'] = _find_estimated_crop_yield(variety_id, year, garden_type=garden_type)
                crop['type_estimated_yield'] = (crop['type_average_yield'] or 0) * (crop['plants'] or 0)
                total_yield_by_garden_type += crop['type_estimated_yield']

        # find estimated dollar value of the crop yield for the given patches
        if estimate_value:
            cost_per_pound = _find_estimated_dollar_value(variety_id, year)
            if not cost_per_pound:
                continue
            crop['estimated_value'] = estimated_value = cost_per_pound * crop['estimated_yield']
            total_value += estimated_value or 0

            # if we have a garden type, find estimated value using that estimated yield
            if garden_type:
                crop['type_estimated_value'] = cost_per_pound * crop['type_estimated_yield']
                total_value_by_garden_type += crop['type_estimated_value']
    return {
        'crops': crops,
        'total_yield': total_yield,
        'total_yield_by_garden_type': total_yield_by_garden_type,
        'total_value': total_value,
        'total_value_by_garden_type': total_value_by_garden_type,
    }

def _estimate_value(variety_id, recorded_date, pounds):
    estimates = EstimatedCost.objects.filter(variety__id=variety_id, valid_start__lte=recorded_date, valid_end__gt=recorded_date, should_be_used=True).order_by('-estimated')
    try:
        return estimates[0].cost_per_pound * pounds
    except:
        return None
