from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
from .forms import (LookingGoodEventForm, LookingGoodItemFormSet,
                    LookingGoodPhotoFormSet)
from .models import LookingGoodEvent


class LookingGoodEventMixin(MetricMixin):
    metric_model = LookingGoodEvent

    def get_metric_name(self):
        return 'Beauty of the Garden'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class LookingGoodEventIndex(LookingGoodEventMixin, IndexView):
    template_name = 'metrics/lookinggood/event/index.html'


class LookingGoodEventAllGardensView(RecordsMixin, TitledPageMixin,
                                     LookingGoodEventMixin, AllGardensView):

    def get_title(self):
        return 'All gardens measuring looking good tags'


class LookingGoodEventGardenDetails(LookingGoodEventMixin,
                                    GardenDetailAddRecordView):
    form_class = LookingGoodEventForm
    template_name = 'metrics/lookinggood/event/garden_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LookingGoodEventGardenDetails, self).get_context_data(
            **kwargs
        )
        if self.request.POST:
            context['photo_formset'] = LookingGoodPhotoFormSet(self.request.POST,
                                                               self.request.FILES)
            context['item_formset'] = LookingGoodItemFormSet(self.request.POST)
        else:
            context['photo_formset'] = LookingGoodPhotoFormSet()
            context['item_formset'] = LookingGoodItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        item_formset = context['item_formset']
        if photo_formset.is_valid() and item_formset.is_valid():
            instance = form.save()
            photo_formset.instance = instance
            photo_formset.save()
            item_formset.instance = instance
            item_formset.save()
            return super(LookingGoodEventGardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_message(self):
        return 'Successfully added looking good tags record to %s' % (
            self.object,
        )
