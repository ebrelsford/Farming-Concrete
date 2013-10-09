from datetime import date

from farmingconcrete.models import Garden
from farmingconcrete.utils import garden_type_label
from generic.views import (LoginRequiredMixin, PermissionRequiredMixin,
                           TitledPageMixin)
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, MetricGardenCSVView, RecordsMixin,
                     UserGardenView)
from .forms import LookingGoodEventForm, LookingGoodTagFormSet
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
            context['tag_formset'] = LookingGoodTagFormSet(self.request.POST)
        else:
            context['tag_formset'] = LookingGoodTagFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tag_formset = context['tag_formset']
        if tag_formset.is_valid():
            tag_formset.instance = form.save()
            tag_formset.save()
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

    def get_filename(self):
        # TODO add year, date retrieved
        return '%s - looking good' % self.garden.name
