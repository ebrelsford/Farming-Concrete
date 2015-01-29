from datetime import date

from dateutil.parser import parse
import tablib

from crops.utils import get_crop, get_variety
from .models import Gardener, Harvest


field_names = {
    'crop': ('crop',),
    'gardener': ('gardener',),
    'harvested': ('date', 'harvested', 'recorded',),
    'variety': ('crop variety', 'variety',),
    'weight': ('pounds', 'quantity', 'weight',),
}


def _get_field_value(row, field):
    for name in field_names[field]:
        try:
            return row[name]
        except Exception:
            continue
    return None


def _get_harvested(row):
    value = _get_field_value(row, 'harvested')
    try:
        return parse(value)
    except Exception:
        return None


def _get_crop(row, create=False):
    value = _get_field_value(row, 'crop')
    # TODO Ignore very generic crop names like "herbs" and "greens"?
    # TODO create, without a user
    return get_crop(value, None)[0]


def _get_variety(row, crop, create=False):
    value = _get_field_value(row, 'variety')

    if not value:
        return None
    try:
        # TODO create, without a user
        return get_variety(value, crop, None)[0]
    except Exception:
        return None


def _get_gardener(row, garden, create=False):
    """
    Attempt to get a gardener for the given row and garden.
    
    Only creates new Gardener instances if create=True.
    """
    gardener_name = _get_field_value(row, 'gardener')

    # Worst case scenario: attempt to find or make a generic gardener
    if not gardener_name:
        gardener_name = 'all gardeners'

    kwargs = {
        'garden': garden,
        'name': gardener_name,
    }

    # Not using get_or_create() here since we only want to create if create=True
    try:
        return Gardener.objects.get(**kwargs)
    except Gardener.DoesNotExist:
        if create:
            gardener = Gardener(**kwargs)
            gardener.save()
            return gardener
    return None


def _get_weight(row):
    try:
        return float(_get_field_value(row, 'weight'))
    except Exception:
        return None


def load(filename, garden, create_crops=False, create_gardeners=False,
         create_varieties=False, dry_run=False, verbose=True):
    # Load file
    harvests = tablib.Dataset()
    harvests.csv = open(filename, 'r').read()

    # For each record create a harvest
    for row in harvests.dict:
        crop = _get_crop(row, create=create_crops)
        gardener = _get_gardener(row, garden, create=create_gardeners)
        harvested = _get_harvested(row)
        variety = _get_variety(row, crop, create=create_varieties)
        weight = _get_weight(row)

        if verbose:
            print row
            print crop, gardener, harvested, weight, variety
            print

        if not dry_run:
            harvest = Harvest(
                crop=crop,
                crop_variety=variety,
                gardener=gardener,
                harvested=harvested,
                weight=weight,
            )
            harvest.save()
