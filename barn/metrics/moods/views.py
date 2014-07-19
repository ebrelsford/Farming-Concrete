from farmingconcrete.models import Garden
from generic.views import TitledPageMixin
from ..views import (AllGardensView, GardenDetailAddRecordView, IndexView,
                     MetricMixin, RecordsMixin)
from .forms import MoodChangeForm, MoodCountFormSet
from .models import Mood, MoodChange


class MoodChangeMixin(MetricMixin):
    metric_model = MoodChange

    def get_metric_name(self):
        return 'Good Moods in the Garden'

    def get_all_gardens_with_records(self):
        return Garden.objects.filter(
            pk__in=self.get_records().values_list('garden__pk', flat=True)
        ).distinct().order_by('name')


class MoodChangeIndex(MoodChangeMixin, IndexView):
    template_name = 'metrics/moods/change/index.html'


class MoodChangeAllGardensView(RecordsMixin, TitledPageMixin, MoodChangeMixin,
                               AllGardensView):

    def get_title(self):
        return 'All gardens measuring good moods in the garden'


class MoodChangeGardenDetails(MoodChangeMixin, GardenDetailAddRecordView):
    form_class = MoodChangeForm
    template_name = 'metrics/moods/change/garden_detail.html'

    def get_initial_mood_counts(self):
        initial = []
        for counted_time in ('in', 'out'):
            for mood in Mood.objects.all():
                initial.append({
                    'mood': mood,
                    'count': 0,
                    'counted_time': counted_time,
                })
        return initial

    def get_context_data(self, **kwargs):
        context = super(MoodChangeGardenDetails, self).get_context_data(**kwargs)
        if self.request.POST:
            context['moodcount_formset'] = MoodCountFormSet(self.request.POST)
        else:
            context['moodcount_formset'] = MoodCountFormSet(
                initial=self.get_initial_mood_counts(),
            )
        context['moods'] = Mood.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        moodcount_formset = context['moodcount_formset']
        if moodcount_formset.is_valid():
            moodcount_formset.instance = form.save()
            moodcount_formset.save()
            return super(MoodChangeGardenDetails, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_message(self):
        return 'Successfully added moods in the garden record to %s' % (
            self.object,
        )
