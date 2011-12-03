from datetime import datetime

from django.db.models import Max, Sum

from farmingconcrete.models import Variety
from harvestcount.models import Harvest
from models import EstimatedYield

def make_all_yield_estimates(start, end, by_gardener=True):
    varieties = Variety.objects.filter(harvest__harvested__gte=start, harvest__harvested__lt=end).distinct()
    for variety in varieties:
        pounds_per_plant = _find_yield_estimate(variety, start, end, by_gardener)
        estimated_yield = EstimatedYield(
            variety=variety, 
            estimated=datetime.now(), 
            notes="added via admin", 
            should_be_used=True, 
            pounds_per_plant=str(pounds_per_plant),
            valid_start=start,
            valid_end=end
        )
        estimated_yield.save()

def _find_yield_estimate(variety, start, end, _by_gardener=True):
    """Find an estiated yield for the given variety using harvests recorded in the given date range"""

    # get total weight, maximum plants by gardener
    results = Harvest.objects.filter(variety=variety, harvested__gte=start, harvested__lt=end).values('gardener').annotate(pounds=Sum('weight'), plants=Max('plants'))
    averages = []

    results = [r for r in results if r['pounds'] and r['plants']]

    for result in results:
        pounds = result['pounds']
        plants = result['plants']
        average = float(pounds) / float(plants)
        averages.append(average)

    total_plants = sum([float(result['plants']) for result in results])

    if _by_gardener and averages:
        average = sum(averages) / len(averages)
    elif not _by_gardener and total_plants:
        total_pounds = sum([float(result['pounds']) for result in results])
        average = total_pounds / total_plants
    else:
        average = 0

    return average
