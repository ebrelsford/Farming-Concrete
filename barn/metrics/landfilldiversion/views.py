from datetime import date

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import SuccessMessageFormMixin, TitledPageMixin
from ..views import (AllGardensView, GardenMixin, IndexView, MetricMixin,
                     RecordsMixin, UserGardenView)
from .forms import LandfillDiversionWeightForm
from .models import LandfillDiversionWeight


class WeightMixin(MetricMixin):

    def get_metric_name(self):
        return 'Landfill Diversion by Weight'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class WeightIndex(WeightMixin, IndexView):
    metric_model = LandfillDiversionWeight


class WeightAllGardensView(RecordsMixin, TitledPageMixin, WeightMixin,
                           AllGardensView):
    metric_model = LandfillDiversionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens weighing landfill diversion' %
                garden_type_label(garden_type))


class WeightUserGardensView(TitledPageMixin, WeightMixin, UserGardenView):
    metric_model = LandfillDiversionWeight

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class WeightGardenDetails(SuccessMessageFormMixin, WeightMixin, GardenMixin,
                          FormView):
    form_class = LandfillDiversionWeightForm
    metric_model = LandfillDiversionWeight
    template_name = 'metrics/landfilldiversion/gardens/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(WeightGardenDetails, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(WeightGardenDetails, self).post(request, *args, **kwargs)

    def get_success_message(self):
        return 'Successfully added %.1f pounds to %s' % (self.record.weight,
                                                         self.object)

    def get_success_url(self):
        return reverse('landfilldiversion_weight_garden_details', kwargs={
            'pk': self.object.pk,
        })

    def form_valid(self, form):
        self.record = form.save()
        return super(WeightGardenDetails, self).form_valid(form)

    def get_initial(self):
        garden = self.object

        initial = super(WeightGardenDetails, self).get_initial()
        initial.update({
            'added_by': self.request.user,
            'garden': garden,
            'recorded': date.today(), # TODO get last recorded date if there is one
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super(WeightGardenDetails, self).get_context_data(**kwargs)

        garden = self.object
        records = self.get_records()

        context.update({
            'form': self.get_form(self.form_class),
            'garden': garden,
            'records': records.order_by('recorded'),
            'summary': LandfillDiversionWeight.summarize(records),
        })
        return context
