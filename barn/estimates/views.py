from django.db.models import Count, Max, Min, Sum
from django.views.generic import TemplateView

from farmingconcrete.models import Garden
from metrics.harvestcount.models import Harvest


class ExplainEstimatedYieldView(TemplateView):
    """Show the data used to find the average yield for a given crop."""
    template_name = 'estimates/estimatedyield_explain.html'

    def get_context_data(self, **kwargs):
        context = super(ExplainEstimatedYieldView, self).get_context_data(**kwargs)

        crop_name = self.request.GET.get('crop', None)
        year = self.request.GET.get('year', None)

        harvests = Harvest.objects.filter(
            reportable=True,
            crop__name=crop_name,
            harvested__year=year,
            weight__gt=0,
            plants__gt=0,
        )

        gardeners = list(set([h.gardener for h in harvests]))
        gardener_harvests = {}

        for gardener in gardeners:
            summary = harvests.filter(gardener=gardener).aggregate(
                Min('weight'),
                Max('weight'),
                Min('plants'),
                Max('plants'),
                Min('harvested'),
                Max('harvested'),
                total_harvests=Count('id'),
                total_weight=Sum('weight'),
            )
            summary['average'] = (float(summary['total_weight']) /
                                  float(summary['plants__max']))
            gardener_harvests[gardener] = summary

        context.update({
            'gardens': Garden.objects.filter(gardener__in=gardeners).distinct(),
            'gardener_harvests': gardener_harvests,
            'crop_name': crop_name,
            'year': year,
        })
        return context
