from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from units.convert import system_weight_units
from ..export import MetricDatasetMixin
from .models import Donation


class DonationDatasetMixin(object):
    produce_name = Field(header='produce name')

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
        super(DonationDatasetMixin, self).__init__(**kwargs)

    class Meta:
        model = Donation


class DonationDataset(DonationDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicDonationDataset(DonationDatasetMixin, PublicMetricDatasetMixin,
                            ModelDataset):
    pass
