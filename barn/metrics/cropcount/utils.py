from .models import Patch

#
# Average plants per square foot as collected by Megan Gregory in 2010.
#
PLANTS_BY_AREA_AVERAGES = {
    'beans': 1.588076118,
    'beans (bush)': 1.588076118,
    'calaloo': 1.885119048,
    'cucumbers': 0.897648539,
    'collard greens': 0.881914476,
    'kale': 1.499268776,
    'lettuce': 2.574,
    'peppers (sweet)': 1.11918217,
    'swiss chard': 1.455252839,
    'watermelon': 0.328761234,
    'tomatoes': 0.581187265,
}


def add_estimated_plants(year=2012):
    """
    For patches with area but no plants, estimate the number of plants that
    would have been in that area.

    """
    for variety in PLANTS_BY_AREA_AVERAGES.keys():
        add_estimated_plants_for_variety(variety, year)


def add_estimated_plants_for_variety(variety, year=2012):
    average_plants = PLANTS_BY_AREA_AVERAGES[variety]
    patches = Patch.objects.filter(added__year=2012, variety__name=variety,
                                   plants__isnull=True)
    for patch in patches:
        patch.plants = int(round(float(patch.area) * average_plants))
        patch.estimated_plants = True
        patch.save()
