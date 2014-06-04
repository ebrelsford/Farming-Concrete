from datetime import date

from django.conf import settings
from django.db.models import Min, Sum

from models import EstimatedCost, EstimatedYield


def _find_estimated_crop_yield(crop_id, year, garden_type=None):
    """
    Find the most recent valid EstimatedYield in the year given for the
    crop/garden type given.
    """
    try:
        yields = EstimatedYield.objects.filter(
            crop__id=crop_id,
            valid_start__year=year,
            should_be_used=True
        ).order_by('-estimated')
        if garden_type:
            yields = yields.filter(garden_type=garden_type)
        return yields[0].pounds_per_plant
    except:
        return None


def _find_estimated_dollar_value(variety_id, year):
    try:
        estimates = EstimatedCost.objects.filter(
            variety__id=variety_id,
            valid_start__year=year,
            should_be_used=True
        ).order_by('-estimated')
        return estimates[0].cost_per_pound
    except:
        return None


def estimate_for_harvests_by_gardener_and_variety(harvests):
    """
    Estimate value of harvests for the given harvests, grouped by gardener and
    variety
    """
    gardener_variety_weights = harvests.values(
        'variety__id',
        'variety__name',
        'gardener__garden__name',
        'gardener__garden__id',
        'gardener__name'
    ).annotate(pounds=Sum('weight')).distinct()
    total_value = 0
    gardener_totals = {}
    crop_totals = {}
    garden_totals = {}
    garden_ids = set()

    for row in gardener_variety_weights:
        crop = row['variety__name']
        gardener = row['gardener__name']
        garden = row['gardener__garden__name']
        garden_ids.add(row['gardener__garden__id'])
        weight = row['pounds']
        if gardener not in gardener_totals:
            gardener_totals[gardener] = dict(value=0, weight=0)
        if crop not in crop_totals:
            crop_totals[crop] = dict(value=0, weight=0)
        if garden not in garden_totals:
            garden_totals[garden] = dict(value=0, weight=0)

        row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(settings.FARMINGCONCRETE_YEAR, 6, 1), weight)

        gardener_totals[gardener]['value'] += estimated_value or 0
        gardener_totals[gardener]['weight'] += weight or 0
        crop_totals[crop]['value'] += estimated_value or 0
        crop_totals[crop]['weight'] += weight or 0
        try:
            garden_totals[garden]['gardeners'].add(gardener)
        except KeyError:
            garden_totals[garden]['gardeners'] = set()
            garden_totals[garden]['gardeners'].add(gardener)
        garden_totals[garden]['value'] += estimated_value or 0
        garden_totals[garden]['weight'] += weight or 0
        total_value += estimated_value or 0

    return {
        'gardener_variety_weights': gardener_variety_weights,
        'gardener_totals': gardener_totals,
        'crop_totals': crop_totals,
        'garden_totals': garden_totals,
        'garden_ids': garden_ids,
        'total_value': total_value,
    }


def estimate_for_harvests(harvests, estimate_value=False):
    rows = harvests.values('variety__id', 'variety__name').annotate(
        pounds=Sum('weight')
    ).distinct()
    total_value = 0
    for row in rows:
        if estimate_value:
            row['estimated_value'] = estimated_value = _estimate_value(row['variety__id'], date(settings.FARMINGCONCRETE_YEAR, 6, 1), row['pounds'])
            total_value += estimated_value

    return {
        'rows': rows,
        'total_value': total_value,
    }


def estimate_for_patches(patches, estimate_yield=False, estimate_value=False,
                         garden_type=None):
    """
    Estimate the pounds yielded by the given patches, including a total of all
    patches.
    """
    #
    # Try to get sum of plants/area by crop for the patches given.
    #
    # This is slightly complicated by our desire to make estimates valid only
    # for certain dates.
    #
    crops = patches.values(
        'crop__id',
        'crop__name',
        'box__garden__name',
        'box__garden__id').annotate(
            plants=Sum('plants'),
            area=Sum('area'),
            min_added=Min('added')
        ).distinct()

    total_plants_with_yields = 0
    total_value = 0
    total_value_by_garden_type = 0
    total_yield = 0
    total_yield_by_garden_type = 0
    crop_totals = {}
    garden_totals = {}
    garden_ids = set()

    for crop in crops:
        # For now only use year. Could make this an option or use multiple
        # functions.
        year = crop['min_added'].year
        crop_id = crop['crop__id']
        crop_name = crop['crop__name']
        if crop_name not in crop_totals:
            crop_totals[crop_name] = dict(
                area=0,
                plants=0,
                value=0,
                estimated_yield=0,
                type_estimated_value=None,
                type_average_yield=None,
                type_estimated_yield=None
            )
        garden_name = crop['box__garden__name']
        garden_ids.add(crop['box__garden__id'])
        if garden_name not in garden_totals:
            garden_totals[garden_name] = dict(value=0, weight=0)

        # Find average/estimate overall yield for the patches given containing
        # this crop.
        if estimate_yield:
            crop['average_yield'] = _find_estimated_crop_yield(crop_id, year)
            crop['estimated_yield'] = estimated_yield = (crop['average_yield'] or 0) * (crop['plants'] or 0)
            total_yield += estimated_yield or 0
            garden_totals[garden_name]['weight'] += estimated_yield or 0
            crop_totals[crop_name]['average_yield'] = crop['average_yield']
            crop_totals[crop_name]['estimated_yield'] += crop['estimated_yield']
            crop_totals[crop_name]['plants'] += crop['plants'] or 0
            crop_totals[crop_name]['area'] += crop['area'] or 0

            if crop['average_yield']:
                total_plants_with_yields += crop['plants'] or 0

            # If we have a garden type, get average/estimate for that type
            if garden_type:
                crop['type_average_yield'] = _find_estimated_crop_yield(crop_id, year, garden_type=garden_type)
                crop['type_estimated_yield'] = (crop['type_average_yield'] or 0) * (crop['plants'] or 0)
                crop_totals[crop_name]['type_average_yield'] = crop['type_average_yield']
                crop_totals[crop_name]['type_estimated_yield'] = crop['type_estimated_yield']
                total_yield_by_garden_type += crop['type_estimated_yield']

        # Find estimated dollar value of the crop yield for the given patches
        if estimate_value:
            cost_per_pound = _find_estimated_dollar_value(crop_id, year)
            if not cost_per_pound:
                continue
            crop['estimated_value'] = estimated_value = cost_per_pound * crop['estimated_yield']
            total_value += estimated_value or 0
            garden_totals[garden_name]['value'] += estimated_value or 0
            crop_totals[crop_name]['value'] += estimated_value or 0

            # if we have a garden type, find estimated value using that estimated yield
            if garden_type:
                crop['type_estimated_value'] = cost_per_pound * crop['type_estimated_yield']
                crop_totals[crop_name]['type_estimated_value'] += crop['type_estimated_value']
                total_value_by_garden_type += crop['type_estimated_value']

    crop_totals_t = []
    for crop in crop_totals:
        crop_totals_t.append({
            'name': crop,
            'area': crop_totals[crop]['area'],
            'average_yield': crop_totals[crop]['average_yield'],
            'estimated_yield': crop_totals[crop]['estimated_yield'],
            'plants': crop_totals[crop]['plants'],
            'type_estimated_value': crop_totals[crop]['type_estimated_value'],
            'type_average_yield': crop_totals[crop]['type_average_yield'],
            'type_estimated_yield': crop_totals[crop]['type_estimated_yield'],
            'value': crop_totals[crop]['value'],
        })

    return {
        'crops': crops,
        'total_yield': total_yield,
        'total_yield_by_garden_type': total_yield_by_garden_type,
        'total_value': total_value,
        'total_value_by_garden_type': total_value_by_garden_type,
        'total_plants_with_yields': total_plants_with_yields,
        'garden_totals': garden_totals,
        'garden_ids': garden_ids,
        'crop_totals': crop_totals_t,
    }


def _estimate_value(crop_id, recorded_date, pounds):
    estimates = EstimatedCost.objects.filter(crop__id=crop_id, valid_start__lte=recorded_date, valid_end__gt=recorded_date, should_be_used=True).order_by('-estimated')
    try:
        return estimates[0].cost_per_pound * pounds
    except:
        return None
