from django.forms import ModelForm, HiddenInput, ModelChoiceField, TextInput

from floppyforms.widgets import Select

from crops.forms import AddNewCropWidget, VarietyField
from crops.models import Crop, Variety
from farmingconcrete.models import Garden

from ..forms import RecordForm, RecordedField
from .models import Gardener, Harvest


class AddNewGardenerWidget(Select):
    template_name = 'metrics/harvestcount/gardeners/new_gardener_widget.html'


class GardenerForm(ModelForm):
    garden = ModelChoiceField(queryset=Garden.objects.all(), widget=HiddenInput())

    class Meta:
        model = Gardener
        exclude = ('added_by', 'updated_by')


class HarvestForm(RecordForm):
    recorded = RecordedField(label='Date')
    crop = ModelChoiceField(
        label="Crop name",
        queryset=Crop.objects.filter(needs_moderation=False),
        error_messages={
            'required': "Please enter a crop name",
        },
        widget=AddNewCropWidget(),
    )
    crop_variety = VarietyField(
        queryset=Variety.objects.filter(needs_moderation=False),
        required=False,
    )

    def __init__(self, initial={}, *args, **kwargs):
        super(HarvestForm, self).__init__(initial=initial, *args, **kwargs)
        garden = initial.get('garden', None)

        # Only get gardeners of this garden
        self.fields['gardener'].queryset = self.get_gardeners(garden)

    def get_gardeners(self, garden):
        return Gardener.objects.filter(garden=garden).order_by('name')

    class Meta:
        model = Harvest
        exclude = ('added',)
        widgets = {
            'area': TextInput(attrs={'size': 5, 'maxlength': 5}),
            'gardener': AddNewGardenerWidget(),
            'plants': TextInput(attrs={'size': 5, 'maxlength': 5}),
        }


def get_gardener(name, garden, user):
    """Get a gardener with the given name, creating it if necessary"""
    if not name or not garden or not user:
        return None

    # try to find an already-existing gardener with that name
    gardeners = Gardener.objects.filter(name__iexact=name, garden=garden)
    if gardeners:
        return gardeners[0]

    # else create one
    gardener = Gardener(name=name, added_by=user, garden=garden)
    gardener.save()
    return gardener
