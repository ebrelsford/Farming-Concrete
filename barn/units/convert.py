from collections import Counter

from measurement.measures import Weight
from pint import UnitRegistry


ureg = UnitRegistry()


def find_preferred_measurement_system(gardens):
    """
    For the given garden(s), find the preferred measurement system
    """
    try:
        return Counter([g.measurement_system for g in gardens if g]).most_common()[0][0]
    except IndexError:
        # No valid gardens, assume default
        return 'imperial'
    except TypeError:
        # Looks like we only have one garden, return that system
        return gardens.measurement_system


def to_preferred_units(measurement, value, gardens):
    """
    Convert the given value from its stored units to the one the gardens 
    prefer.
    """
    if measurement == Weight:
        return to_preferred_weight_units(value, gardens)
    return None


def preferred_volume_units(gardens, large=True):
    if find_preferred_measurement_system(gardens) == 'imperial':
        if large:
            return 'gallons'
    return 'liters'


def preferred_weight_units(gardens, large=True):
    if find_preferred_measurement_system(gardens) == 'imperial':
        if large:
            return 'pounds'
    return 'kilograms'


def system_volume_units(system):
    if system == 'imperial':
        return 'gallons'
    return 'liters'


def system_weight_units(system):
    if system == 'imperial':
        return 'pounds'
    return 'kilograms'


def round_if_very_close(value):
    """
    Round number up if very close to the next number.

    Makes numbers a bit more smooth after conversion.
    """
    if value % 1 > 0.999:
        return round(value)
    return value


def to_preferred_volume_units(gardens, liters=None, cubic_meters=None,
                              force_large_units=True):
    if liters:
        liters = liters * ureg.liter
    elif cubic_meters:
        ccs = (cubic_meters * (100 ** 3)) * ureg.cubic_centimeters
        liters = ccs.to(ureg.liter)
    else:
        raise ValueError(('to_preferred_volume_units requires liters or '
                          'cubic_meters'))

    # Imperial
    if find_preferred_measurement_system(gardens) == 'imperial':
        return liters.to(ureg.gallon)

    # Metric
    return liters


def to_weight_units(value, system, force_large_units=True):
    grams = value * ureg.gram

    # Imperial
    if system == 'imperial':
        pounds = grams.to(ureg.pound)
        if force_large_units or round_if_very_close(pounds.magnitude) >= 1:
            return pounds
        return grams.to(ureg.ounce)

    # Metric
    if force_large_units or round_if_very_close(grams.magnitude) >= 1000:
        return grams.to(ureg.kg)
    return grams


def to_preferred_weight_units(value, gardens, force_large_units=True):
    return to_weight_units(value, find_preferred_measurement_system(gardens),
                           force_large_units=force_large_units)
