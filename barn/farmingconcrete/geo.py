import geojson
from pygeocoder import Geocoder

from .models import Garden


def garden_collection(gardens):
    """Get GeoJSON FeatureCollection for the given gardens"""
    return geojson.FeatureCollection(features=[garden_feature(g) for g in gardens])


def garden_feature(garden):
    """Get a geojson Feature for a garden"""
    return geojson.Feature(
        garden.id,
        geometry=geojson.Point(
            coordinates=(float(garden.longitude), float(garden.latitude))
        ),
        properties={
            'name': garden.name,
        }
    )


def fetch_geo_details(garden):
    """Reverse geocode to get garden's state, city, etc"""
    results = Geocoder.reverse_geocode(garden.latitude, garden.longitude)
    address_components = results[0].data[0]['address_components']

    for component in address_components:
        # Borough
        if 'sublocality' in component['types']:
            borough = component['long_name']
            if not garden.borough and borough in [b[0] for b in Garden.BOROUGH_CHOICES]:
                garden.borough = component['long_name']

        # City
        if 'locality' in component['types']:
            if not garden.city:
                garden.city = component['long_name']

        # State
        if 'administrative_area_level_1' in component['types']:
            if not garden.state:
                garden.state = component['short_name']

        # Zip
        if 'postal_code' in component['types']:
            if not garden.zip:
                garden.zip = component['long_name']

    garden.save()
