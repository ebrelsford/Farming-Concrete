from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import LookingGoodEventForm, LookingGoodPhotoFormSet
from .models import LookingGoodEvent


class LookingGoodEventMixin(MetricMixin):
    metric_model = LookingGoodEvent

    def get_metric_name(self):
        return 'Looking Good'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class LookingGoodEventIndex(LookingGoodEventMixin, IndexView):
    template_name = 'metrics/lookinggood/event/index.html'


class LookingGoodEventAllGardensView(RecordsMixin, TitledPageMixin,
                                     LookingGoodEventMixin, AllGardensView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return ('All %s gardens measuring looking good tags' %
                garden_type_label(garden_type))


class LookingGoodEventUserGardensView(TitledPageMixin, LookingGoodEventMixin,
                                      UserGardenView):

    def get_title(self):
        garden_type = self.request.session.get('garden_type', 'all')
        return 'Your %s gardens' % garden_type_label(garden_type)


class LookingGoodEventGardenDetails(LookingGoodEventMixin,
                                    GardenDetailAddRecordView):
    form_class = LookingGoodEventForm
    template_name = 'metrics/lookinggood/event/garden_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LookingGoodEventGardenDetails, self).get_context_data(
            **kwargs
        )
        if self.request.POST:
            context['photo_formset'] = LookingGoodPhotoFormSet(self.request.POST)
        else:
            context['photo_formset'] = LookingGoodPhotoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        if photo_formset.is_valid():
            photo_formset.instance = form.save()
            photo_formset.save()
            return super(LookingGoodEventGardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_message(self):
        return 'Successfully added looking good tags record to %s' % (
            self.object,
        )

    def get_initial(self):
        initial = super(LookingGoodEventGardenDetails, self).get_initial()
        initial.update({
            # TODO get last recorded date if there is one
            'recorded': date.today(),
        })
        return initial


class LookingGoodEventGardenCSV(LookingGoodEventMixin, MetricGardenCSVView):

    def get_fields(self):
        return ('recorded', 'start_time', 'end_time', 'total_tags',)
