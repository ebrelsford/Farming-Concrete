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
    try:
        return float(data.json()['history']['dailysummary'][0]['precipi'])
    except Exception:
        return 0


def get_station(latlng, start, end):
    # TODO save to garden?
    stations = []
    buffer = .2

    while not stations:
        stations = get_stations_buffer(latlng, start, end, buffer=buffer)
        buffer *= 2

    # TODO then find the closest
    #  calculate distance between each
    #  smallest distance
    return stations


def get_stations_buffer(latlng, start, end, buffer=.2):
    lat, lng = latlng
    extent = [
        lat - buffer,
        lng - buffer,
        lat + buffer,
        lng + buffer,
    ]
    params = {
        'extent': extent,
        'datasetid': 'GHCND',
        'datatypeid': 'PRCP',
        'startdate': start.strftime('%Y-%m-%d'),
        'enddate': end.strftime('%Y-%m-%d'),
    }
    headers = {
        'token': 'XXX token here',
    }
    url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    try:
        return requests.get(url, params=params, headers=headers).json()['results']
    except Exception:
        return []
