from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import (ModelForm, HiddenInput, ModelChoiceField, TextInput,
                          CharField, ChoiceField, DecimalField, DateField)
from django.forms.models import inlineformset_factory

from farmingconcrete.forms import AddNewVarietyWidget
from farmingconcrete.models import Garden, Variety
from ..forms import RecordedInput
from .models import Box, Patch


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
        label="Bed #"
    )
    length = BedSizeField()
    width = BedSizeField(label='Dimensions (feet)')

    recorded = DateField(
        label='Recorded',
        widget=RecordedInput,
    )

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
        widget=HiddenInput(),
    )
    variety = ModelChoiceField(
        label="Crop name",
        queryset=Variety.objects.filter(needs_moderation=False),
        error_messages={
            'required': "Please enter a plant type.",
        },
        widget=AddNewVarietyWidget(),
    )
    quantity = DecimalField(
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
    )
    units = ChoiceField(
        choices = Patch.UNITS_CHOICES,
    )
    added_by = ModelChoiceField(
        label='added_by',
        queryset=User.objects.all(),
        widget=HiddenInput()
    )

    class Meta:
        model = Patch
        exclude = ('added', 'area', 'plants', 'updated')


PatchFormSet = inlineformset_factory(Box, Patch,
    can_delete=False,
    extra=1,
    form=PatchForm,
)
