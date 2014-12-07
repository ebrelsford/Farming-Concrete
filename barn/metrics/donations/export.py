from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import Donation


class DonationDatasetMixin(object):
    produce_name = Field(header='produce name')

    class Meta:
        model = Donation
        fields = ['produce_name', 'pounds',]


class DonationDataset(DonationDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicDonationDataset(DonationDatasetMixin, PublicMetricDatasetMixin,
                            ModelDataset):
    pass
