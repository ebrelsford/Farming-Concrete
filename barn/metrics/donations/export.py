from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import Donation


class DonationDataset(MetricDatasetMixin, ModelDataset):
    produce_name = Field(header='produce name')

    class Meta:
        model = Donation
        fields = ['produce_name', 'pounds',]
