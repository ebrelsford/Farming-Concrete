import math
from pint import UnitRegistry
import requests

from django.conf import settings


GALLONS_PER_SF = 0.6
HARVESTING_EFFICIENCY = 0.75
NOAA_DATA_URL = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data'
NOAA_STATIONS_URL = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/stations'

ureg = UnitRegistry()


def calculate_rainwater_gallons(latlng, length, width, start, end):
    station = get_station(latlng, start, end)
    rainfall = get_rainfall_total(station, start, end)
    return rainfall * length * width * GALLONS_PER_SF * HARVESTING_EFFICIENCY


def get_rainfall_total(station, start, end):
    """Get the rainfall total in inches"""
    entries = get_rainfall_entries(station, start, end)
    total = sum(map(lambda e: e['value'], entries))

    # Convert from tenths of millimeters to inches
    return ((total / 10.0) * ureg.mm).to(ureg.inches).magnitude


def get_rainfall_entries(station, start, end):
    """Get all rainfall entries for a station and timeframe"""
    params = {
        'stationid': station['id'],
        'datasetid': 'GHCND',
        'datatypeid': 'PRCP',
        'startdate': start.strftime('%Y-%m-%d'),
        'enddate': end.strftime('%Y-%m-%d'),
        'limit': 500,
    }
    headers = {
        'token': settings.NOAA_TOKEN,
    }
    return requests.get(NOAA_DATA_URL, params=params, headers=headers).json()['results']


def get_station(latlng, start, end):
    """
    Get an appropriate station for the given location looking for data in the
    given timeframe.
    """
    # TODO save to garden?
    stations = []
    buffer = .2

    latlng = [float(c) for c in latlng]
    while not stations:
        stations = get_stations_buffer(latlng, start, end, buffer=buffer)
        buffer *= 2

    def distance(station):
        return math.sqrt(abs(latlng[0] - station['latitude']) ** 2 +
                         abs(latlng[1] - station['longitude']) ** 2)
    return min(stations, key=distance)


def get_stations_buffer(latlng, start, end, buffer=.2):
    """Find all stations within a given buffer of a location"""
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
        'token': settings.NOAA_TOKEN,
    }
    return requests.get(NOAA_STATIONS_URL, params=params, headers=headers).json()['results']
