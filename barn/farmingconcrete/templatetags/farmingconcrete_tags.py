from collections import OrderedDict

from django import template
from django.db.models import Sum

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag

from farmingconcrete.models import Garden, GardenType
from metrics.compost.models import CompostProductionWeight
from metrics.harvestcount.models import Harvest
from units.convert import to_weight_units

register = template.Library()


class Overview(AsTag):
    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_cities(self):
        cities = Garden.objects.filter(
            has_metric_records=True,
            city__isnull=False
        ).exclude(city='').values_list( 'city', 'state').distinct()
        return len(cities)

    def get_compost_pounds(self):
        grams = CompostProductionWeight.objects.aggregate(grams=Sum('weight'))['grams']
        return round(to_weight_units(grams, 'imperial').magnitude)

    def get_food_pounds(self):
        grams = Harvest.objects.aggregate(grams=Sum('weight'))['grams']
        return round(to_weight_units(grams, 'imperial').magnitude)

    def get_value(self, context):
        context.update({
            'cities': self.get_cities(),
            'gardens': Garden.objects.filter(has_metric_records=True).count(),
            'pounds_of_compost': self.get_compost_pounds(),
            'pounds_of_food': self.get_food_pounds(),
        })
        return context


class GardenTypes(AsTag):
    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context):
        return GardenType.objects.all().order_by('name')


class GardenTypeDescriptions(InclusionTag):
    template = 'farmingconcrete/garden_type_descriptions.html'

    def get_context(self, context):
        descriptions = OrderedDict()
        for garden_type in GardenType.objects.all().order_by('name'):
            descriptions[garden_type.name] = garden_type.description
        context['garden_types'] = descriptions
        return context


register.tag(Overview)
register.tag(GardenTypes)
register.tag(GardenTypeDescriptions)
