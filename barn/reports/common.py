
from cropcount.models import Patch
from farmingconcrete.models import Garden
from harvestcount.models import Harvest


def filter_harvests(garden=None, borough=None, neighborhood=None, type=None,
                    year=None, variety=None):
    """Get valid harvests for the given garden"""
    harvests = Harvest.objects.filter(harvested__year=year)
    if garden:
        return harvests.filter(gardener__garden=garden)
    if borough:
        harvests = harvests.filter(gardener__garden__borough=borough)
    if neighborhood:
        harvests = harvests.filter(gardener__garden__neighborhood=neighborhood)
    if type:
        harvests = harvests.filter(gardener__garden__type__name=type)
    if variety:
        harvests = harvests.filter(variety__name__iexact=variety)

    return harvests.distinct()


def filter_patches(garden=None, borough=None, neighborhood=None, type=None,
                   year=None, use_all_cropcount=False, variety=None):
    """Get valid patches for the given garden"""
    patches = Patch.objects.filter(added__year=year)
    gardens_last_year = Garden.objects.exclude(box__patch__added__year=year).filter(box__patch__added__year=(int(year)-1))

    if variety:
        patches = patches.filter(variety__name__iexact=variety)

    if garden:
        patches = patches.filter(box__garden=garden)
    else:
        if borough:
            patches = patches.filter(box__garden__borough=borough)
            gardens_last_year = gardens_last_year.filter(borough=borough)
        if neighborhood:
            patches = patches.filter(box__garden__neighborhood=neighborhood)
        if type:
            patches = patches.filter(box__garden__type__name=type)
            gardens_last_year = gardens_last_year.filter(type__name=type)
        if use_all_cropcount:
            patches = patches | Patch.objects.filter(box__garden__in=gardens_last_year)

    return patches.distinct()


def participating_gardens(year):
    cropcount_gardens = Garden.objects.filter(box__patch__added__year=year)
    harvestcount_gardens = Garden.objects.filter(gardener__harvest__harvested__year=year)
    return (cropcount_gardens | harvestcount_gardens).distinct()


def filter_boroughs(year):
    """get the boroughs with participating gardens for the given year"""
    return (participating_gardens(year)).values_list('borough', flat=True).order_by('borough').distinct()


def filter_neighborhoods(year, include_borough=True):
    """Get the neighborhoods for the given year"""
    return (participating_gardens(year)).values('neighborhood', 'borough').order_by('neighborhood').distinct()


def filter_varieties(year):
    """Get the varieties for the given year"""
    patches = filter_patches(year=year)
    return patches.values_list('variety__name', flat=True).order_by('variety__name').distinct()


def get_garden_counts_by_type(harvest_totals, crop_totals):
    garden_names = set(harvest_totals.keys() + crop_totals.keys())

    # TODO don't assume name is unique
    gardens = [Garden.objects.get(name=n) for n in garden_names]
    counts_by_type = {}
    for garden in gardens:
        counts_by_type[garden.type] = counts_by_type.get(garden.type, 0) + 1
    return counts_by_type


def consolidate_totals(harvest_totals, crop_totals):
    """
    Smoosh cropcounts and harvestcounts together, preferring cropcounts when
    gardens have them. This gives us a more inclusive picture of numbers,
    since not all gardens have cropcounts.
    """
    gardens = set(harvest_totals.keys() + crop_totals.keys())
    overall_weight = 0
    overall_value = 0
    overall_gardens = []

    for garden in gardens:
        garden_details = {
            'name': garden,
        }

        try:
            garden_details['gardeners'] = len(harvest_totals[garden]['gardeners'])
        except KeyError:
            pass

        # prefer cropcount, assuming it will be more complete
        if garden in crop_totals:
            overall_weight += crop_totals[garden]['weight']
            overall_value += crop_totals[garden]['value']
            garden_details.update({
                'participation': 'cropcount',
                'weight': crop_totals[garden]['weight'],
                'value': crop_totals[garden]['value'],
            })
        else:
            overall_weight += harvest_totals[garden]['weight']
            overall_value += harvest_totals[garden]['value']
            garden_details.update({
                'participation': 'harvestcount',
                'weight': harvest_totals[garden]['weight'],
                'value': harvest_totals[garden]['value'],
            })
        overall_gardens.append(garden_details)

    return {
        'overall_weight': overall_weight,
        'overall_value': overall_value,
        'overall_gardens': overall_gardens,
    }
