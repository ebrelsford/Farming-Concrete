from django_tablib import Field, ModelDataset

from ..export import MetricDatasetMixin
from .models import Sale


class SaleDataset(MetricDatasetMixin, ModelDataset):
    recorded = Field(header='recorded')
    product = Field(header='product')
    unit = Field(header='unit')
    unit_price = Field(header='unit price ($)')
    units_sold = Field(header='units sold')
    total_price = Field(header='total price ($)')

    class Meta:
        model = Sale
        field_order = (
            'recorded',
            'added_by_display',
            'product',
            'unit',
            'unit_price',
            'units_sold',
            'total_price',
        )
