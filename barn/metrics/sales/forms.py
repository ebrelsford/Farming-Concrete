from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm

from farmingconcrete.models import Garden
from ..forms import RecordedInput
from .models import Sale


class SaleForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = Sale
        fields = ('product', 'unit', 'unit_price', 'units_sold', 'total_price',
                  'recorded', 'added_by', 'garden',)
        widgets = {
            'recorded': RecordedInput(),
        }

