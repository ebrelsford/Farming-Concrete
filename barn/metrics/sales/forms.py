from ..forms import RecordForm, RecordedField
from .models import Sale


class SaleForm(RecordForm):
    recorded = RecordedField(label='Date')

    class Meta:
        model = Sale
        fields = ('product', 'unit', 'unit_price', 'units_sold', 'total_price',
                  'recorded', 'added_by', 'garden',)
