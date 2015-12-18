from uuid import uuid4

from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from units.convert import system_weight_units
from ..export import MetricDatasetMixin
from .models import Harvest


class HarvestcountDatasetMixin(object):
    gardener = Field(header='gardener')
    crop = Field(header='crop')
    crop_variety = Field(header='crop variety')
    plants = Field(header='plants')
    area = Field(header='area')

    def __init__(self, **kwargs):
        units = system_weight_units(kwargs.get('measurement_system', None))

        self.base_fields.update({
            'weight': Field(attribute='weight_%s' % units,
                            header='weight (%s)' % units)
        })
        self._meta.fields = ['weight',] + self._meta.fields
        if self._meta.field_order:
            self._meta.field_order = ('weight',) + self._meta.field_order
        else:
            self._meta.field_order = ('weight',)
        super(HarvestcountDatasetMixin, self).__init__(**kwargs)

    class Meta:
        model = Harvest
        fields = [
            'recorded',
            'gardener',
            'crop',
            'crop_variety',
            'plants',
            'area',
        ]
        field_order = (
            'recorded',
            'gardener',
            'crop',
            'crop_variety',
            'plants',
            'area',
        )


class HarvestcountDataset(HarvestcountDatasetMixin, MetricDatasetMixin,
                          ModelDataset):
    pass


class PublicHarvestcountDataset(HarvestcountDatasetMixin, 
                                PublicMetricDatasetMixin, ModelDataset):
    gardener_mapping = {}

    def generate_unique_id(self):
        unique_id = str(uuid4()).split('-')[0]
        while not unique_id:
            unique_id = str(uuid4()).split('-')[0]
        return unique_id

    def gardener_unique_id(self, row):
        gardener_name = row[self.headers.index('gardener')]
        try:
            return self.gardener_mapping[gardener_name]
        except KeyError:
            self.gardener_mapping[gardener_name] = self.generate_unique_id()
            return self.gardener_mapping[gardener_name]

    def __init__(self, *args, **kwargs):
        super(PublicHarvestcountDataset, self).__init__(*args, **kwargs)
        try:
            self.append_col(self.gardener_unique_id, header='gardener unique id') 
        except IndexError:
            # Thrown on empty dataset
            pass
        del self['gardener']
