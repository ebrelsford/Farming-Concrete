from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import (ModelForm, HiddenInput, ModelChoiceField, TextInput,
                          CharField, IntegerField, DecimalField, DateField,
                          DateInput)

from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import Garden
from .models import Box, Patch


class RecordedInput(DateInput):
    input_type = 'date'


class BedSizeField(DecimalField):
    def __init__(self, *args, **kwargs):
        super(BedSizeField, self).__init__(
            max_value=Decimal('10000'),
            min_value=Decimal('0.1'),
            max_digits=5,
            decimal_places=2,
            error_messages={
                'required': "Please enter the bed's size.",
                'invalid': "Please enter numbers for the bed's size.",
                'min_value': "Please enter a non-negative number.",
                'max_value': "Please enter a smaller number.",
                'max_digits': "Please enter a smaller number.",
                'max_whole_digits': "Please enter a smaller number (%d digits).",
                'max_decimal_places': ("Please enter a number with at most %d "
                                       "decimal places."),
            },
            widget=TextInput(attrs={'size': 6, 'maxlength': 6}),
            required=False,
            *args, **kwargs
        )


class BoxForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())
    added_by = ModelChoiceField(label='added_by', queryset=User.objects.all(),
                                widget=HiddenInput())

    name = CharField(
        max_length=32,
        error_messages={'required': "Please enter a bed number."},
        widget=TextInput(attrs={'size': 10}),
        label="Number"
    )
    length = BedSizeField()
    width = BedSizeField(label='Size')

    class Meta:
        model = Box
        exclude = ('added', 'updated')

    def clean(self):
        super(BoxForm, self).clean()
        data = self.cleaned_data
        length = data.get('length')
        width = data.get('width')

        # only give one message for missing bed sizes
        if not length or not width:
            raise ValidationError("Please enter the bed's size.")

        return data


class PatchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PatchForm, self).__init__(*args, **kwargs)

    box = ModelChoiceField(
        label='box',
        queryset=Box.objects.all(),
        widget=HiddenInput()
    )
    garden = ModelChoiceField(
        label='garden',
        queryset=Garden.objects.all(),
        widget=HiddenInput()
    )
    recorded = DateField(
        label='recorded',
        widget=RecordedInput,
    )
    variety = AutoCompleteSelectField('variety',
        label="Plant type",
        error_messages={
            'required': "Please enter a plant type.",
        }
    )
    area = DecimalField(
        max_value=Decimal('1000'),
        min_value=Decimal('0.1'),
        max_digits=5,
        decimal_places=2,
        error_messages={
            'invalid': "Please enter a number for the area.",
            'min_value': "Please enter a non-negative number.",
            'max_value': "Please enter a smaller number.",
            'max_digits': "Please enter a smaller number.",
            'max_whole_digits': "Please enter a smaller number (%d digits).",
            'max_decimal_places': ("Please enter a number with at most %d "
                                   "decimal places."),
        },
        widget=TextInput(attrs={'size': 6, 'maxlength': 6}),
        required=False
    )
    plants = IntegerField(
        max_value=Decimal('999'),
        min_value=Decimal('1'),
        error_messages={
            'invalid': "Please enter a number for the number of plants.",
            'min_value': "Please enter a non-negative number.",
            'max_value': "Please enter a smaller number.",
        },
        widget=TextInput(attrs={'size': 3}),
        required=False
    )
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = Patch
        exclude = ('added', 'updated')

    def clean(self):
        super(PatchForm, self).clean()
        data = self.cleaned_data
        plants = data.get('plants')
        area = data.get('area')

        # only give one message for missing bed sizes
        if not plants and not area:
            if not 'plants' in self._errors:
                msg = 'Please either enter the number of plants or the area.'
                self._errors['plants'] = self.error_class([msg])

        return data
