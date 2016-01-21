from uuid import uuid4

from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from units.convert import system_distance_units
from ..export import MetricDatasetMixin
from .models import Patch


class CropcountDatasetMixin(object):
    recorded = Field(header='recorded')
    box = Field(header='bed')
    crop = Field(header='crop')
    crop_variety = Field(header='crop variety')
    quantity = Field(header='quantity')
    units = Field(header='units')

    def __init__(self, *args, **kwargs):
        units = system_distance_units(kwargs.get('measurement_system', None))

        # Add bed dimensions
        self.base_fields.update({
            'bed_length': Field(attribute='bed_length_%s' % units,
                                header='bed length (%s)' % units),
            'bed_width': Field(attribute='bed_width_%s' % units,
                               header='bed width (%s)' % units)
        })
        self._meta.field_order += ('bed_width', 'bed_length',)

        super(CropcountDatasetMixin, self).__init__(*args, **kwargs)

    class Meta:
        model = Patch
        fields = [
            'recorded',
            'box',
            'crop',
            'crop_variety',
            'quantity',
            'units',
        ]
        field_order = (
            'recorded',
            'box',
            'crop',
            'crop_variety',
            'quantity',
            'units',
        )


class CropcountDataset(CropcountDatasetMixin, MetricDatasetMixin, ModelDataset):

    def get_queryset(self):
        return self.model.get_records(
            gardens=self.gardens,
            start=self.start,
            end=self.end
        ).select_related('box', 'crop', 'crop_variety')


class PublicCropcountDataset(CropcountDatasetMixin, PublicMetricDatasetMixin,
                             ModelDataset):
    bed_mapping = {}

    def generate_unique_id(self):
        unique_id = str(uuid4()).split('-')[0]
        while not unique_id:
            unique_id = str(uuid4()).split('-')[0]
        return unique_id

    def bed_unique_id(self, row):
        bed_name = row[self.headers.index('box')] + row[self.headers.index('garden')]
        try:
            return self.bed_mapping[bed_name]
        except KeyError:
            id = self.bed_mapping[bed_name] = self.generate_unique_id()
            return id

    def __init__(self, *args, **kwargs):
        super(PublicCropcountDataset, self).__init__(*args, **kwargs)
        try:
            self.append_col(self.bed_unique_id, header='bed unique id') 
        except IndexError:
            # Thrown on empty dataset
            pass
        del self['box']
