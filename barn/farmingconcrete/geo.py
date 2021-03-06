import geojson
from pygeocoder import Geocoder

from accounts.utils import get_profile
from .models import Garden


def garden_collection(gardens, user=None):
    """Get GeoJSON FeatureCollection for the given gardens"""
    return geojson.FeatureCollection(features=[garden_feature(g, user) for g in gardens])


def garden_feature(garden, user=None):
    """Get a geojson Feature for a garden"""
    is_user_garden = (user and user.is_authenticated() and 
                      get_profile(user).gardens.filter(pk=garden.pk).exists())

    # Round coordinates if user doesn't have access to them
    coordinates = (float(garden.longitude), float(garden.latitude))
    if not (garden.share_location or is_user_garden):
        coordinates = [round(coord, 2) for coord in coordinates]

    # Only show name if user has access to it
    properties = {}
    if garden.share_name or is_user_garden:
        properties['name'] = garden.name
    return geojson.Feature(
        garden.id,
        geometry=geojson.Point(coordinates=coordinates),
        properties=properties
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
