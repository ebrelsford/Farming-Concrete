from itertools import product

from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import Mood, MoodChange


class MoodChangeDatasetMixin(object):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')

    def __init__(self, *args, **kwargs):
        moods = Mood.objects.all().order_by('name').values_list('name', flat=True)
        mood_fields = []
        for (mood, time) in product(moods, ('in', 'out')):
            field_name = '%s_%s' % (str(mood).replace(' ', '_'), time)
            header_name = '%s (%s)' % (mood, time)
            self.base_fields[field_name] = Field(header=header_name)
            mood_fields.append(field_name)

        self._meta.field_order += tuple(mood_fields)
        super(MoodChangeDatasetMixin, self).__init__(*args, **kwargs)

    class Meta:
        model = MoodChange
        fields = [
            'recorded_start',
            'recorded',
        ]
        field_order = (
            'recorded_start',
            'recorded',
        )


class MoodChangeDataset(MoodChangeDatasetMixin, MetricDatasetMixin,
                        ModelDataset):
    pass


class PublicMoodChangeDataset(MoodChangeDatasetMixin, PublicMetricDatasetMixin,
                              ModelDataset):
    pass
