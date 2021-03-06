from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import HoursByGeography, HoursByProject, HoursByTask, Task


class HoursByGeographyDatasetMixin(object):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')
    in_half = Field(header='1/2-hour pins "IN"')
    in_whole = Field(header='1-hour pins "IN"')
    out_half = Field(header='1/2-hour pins "OUT"')
    out_whole = Field(header='1-hour pins "OUT"')

    class Meta:
        model = HoursByGeography
        fields = [
            'recorded_start',
            'recorded',
            'in_half',
            'in_whole',
            'out_half',
            'out_whole',
        ]
        field_order = (
            'recorded_start',
            'recorded',
            'in_half',
            'in_whole',
            'out_half',
            'out_whole',
        )


class HoursByGeographyDataset(HoursByGeographyDatasetMixin, MetricDatasetMixin,
                              ModelDataset):
    pass


class PublicHoursByGeographyDataset(HoursByGeographyDatasetMixin,
                                    PublicMetricDatasetMixin, ModelDataset):
    pass


class HoursByTaskDatasetMixin(object):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')

    def __init__(self, *args, **kwargs):
        tasks = Task.objects.all().order_by('name')
        task_fields = []

        def attrify(task):
            """
            Get an attr string for the task that will work on an HoursByTask
            object.
            """
            return 'task_%d' % task.pk

        # Add all potential tasks
        for task in tasks:
            field_name = attrify(task)
            self.base_fields[field_name] = Field(header=task.name)
            task_fields.append(field_name)
        self._meta.field_order += tuple(task_fields)

        # Add task_other
        self.base_fields['task_other'] = Field(header='other tasks examples')
        self._meta.field_order += ('task_other',)

        super(HoursByTaskDatasetMixin, self).__init__(*args, **kwargs)

    class Meta:
        model = HoursByTask
        fields = [
            'recorded_start',
            'recorded',
        ]
        field_order = (
            'recorded_start',
            'recorded',
        )


class HoursByTaskDataset(HoursByTaskDatasetMixin, MetricDatasetMixin,
                         ModelDataset):
    pass


class PublicHoursByTaskDataset(HoursByTaskDatasetMixin,
                               PublicMetricDatasetMixin, ModelDataset):
    pass


class HoursByProjectDatasetMixin(object):

    class Meta:
        model = HoursByProject
        fields = [
            'recorded',
        ]
        field_order = (
            'recorded',
        )


class HoursByProjectDataset(HoursByProjectDatasetMixin, MetricDatasetMixin,
                            ModelDataset):

    def __init__(self, *args, **kwargs):
        # Add project
        self.base_fields['project'] = Field(header='project')
        self._meta.field_order += ('project',)

        garden = kwargs.get('gardens', [])[0]
        gardeners = garden.gardener_set.all().order_by('name')
        gardener_fields = []

        def attrify(gardener):
            """
            Get an attr string for the gardener that will work on an
            HoursByProject object.
            """
            return 'gardener_%d' % gardener.pk

        # Add all potential gardeners
        for gardener in gardeners:
            field_name = attrify(gardener)
            self.base_fields[field_name] = Field(header=gardener.name)
            gardener_fields.append(field_name)
        self._meta.field_order += tuple(gardener_fields)

        super(HoursByProjectDataset, self).__init__(*args, **kwargs)


class PublicHoursByProjectDataset(HoursByProjectDatasetMixin,
                                  PublicMetricDatasetMixin, ModelDataset):

    def __init__(self, *args, **kwargs):
        # Add total_hours
        self.base_fields['total_hours'] = Field(header='total hours')
        self._meta.field_order += ('total_hours',)

        super(PublicHoursByProjectDataset, self).__init__(*args, **kwargs)
