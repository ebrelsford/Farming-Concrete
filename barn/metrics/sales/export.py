from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import Sale


class SaleDatasetMixin():
    recorded = Field(header='recorded')
    product = Field(header='product')
    unit = Field(header='unit')
    unit_price = Field(header='unit price ($)')
    units_sold = Field(header='units sold')
    total_price = Field(header='total price ($)')

    class Meta:
        model = Sale
        fields = [
            'recorded',
            'product',
            'unit',
            'unit_price',
            'units_sold',
            'total_price',
        ]
        field_order = (
            'recorded',
            'product',
            'unit',
            'unit_price',
            'units_sold',
            'total_price',
        )


class SaleDataset(SaleDatasetMixin, MetricDatasetMixin, ModelDataset):
    pass


class PublicSaleDataset(SaleDatasetMixin, PublicMetricDatasetMixin,
                        ModelDataset):
    pass
