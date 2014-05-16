import requests

from django.conf import settings

from datetime import timedelta


base_url = 'http://api.wunderground.com/api/%(api_key)s/history_%(date)s/q/%(lat)f,%(lng)f.json'

GALLONS_PER_SF = 0.6
HARVESTING_EFFICIENCY = 0.75


def calculate_rainwater_gallons(latlng, length, width, start, end):
    rainfall = sum_rainfall(latlng, start, end)
    return rainfall * length * width * GALLONS_PER_SF * HARVESTING_EFFICIENCY


def sum_rainfall(latlng, start, end):
    """
    Sum the rainfall for a location between two dates.
    """
    if start > end:
        raise ValueError('start must come before end')
    current = start
    rainfall = 0
    one_day = timedelta(1)
    while current <= end:
        rainfall += get_rainfall_history(latlng, current)
        current += one_day
    return rainfall


def get_rainfall_history(latlng, date):
    # XXX can only get up to 10 days per minute
    data = requests.get(base_url % {
        'api_key': settings.WUNDERGROUND_API_KEY,
        'date': date.strftime('%Y%m%d'),
        'lat': latlng[0],
        'lng': latlng[1],
    })
    return float(data.json()['history']['dailysummary'][0]['precipi'])
