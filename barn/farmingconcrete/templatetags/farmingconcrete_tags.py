from django import template
from django.db.models import Sum

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from farmingconcrete.models import Garden
from metrics.compost.models import CompostProductionWeight
from metrics.harvestcount.models import Harvest

register = template.Library()


class Overview(AsTag):
    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_compost_pounds(self):
        pounds = CompostProductionWeight.objects.aggregate(pounds=Sum('weight'))['pounds']
        return round(pounds)

    def get_food_pounds(self):
        pounds = Harvest.objects.aggregate(pounds=Sum('weight'))['pounds']
        return round(pounds)

    def get_value(self, context):
        context.update({
            'gardens': Garden.objects.filter(has_metric_records=True).count(),
            'pounds_of_compost': self.get_compost_pounds(),
            'pounds_of_food': self.get_food_pounds(),
        })
        return context


register.tag(Overview)
