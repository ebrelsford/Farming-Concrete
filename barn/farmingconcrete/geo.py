import geojson


def garden_collection(gardens):
    """Get GeoJSON FeatureCollection for the given gardens"""
    return geojson.FeatureCollection(features=[garden_feature(g) for g in gardens])


def garden_feature(garden):
    """Get a geojson Feature for a garden"""
    return geojson.Feature(
        garden.id,
        geometry=geojson.Point(
            coordinates=(float(garden.longitude), float(garden.latitude))
        )
    )
