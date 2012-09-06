from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, HiddenInput, ModelChoiceField, TextInput, DateInput, ValidationError

from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import Garden
from farmingconcrete.utils import get_variety
from models import Gardener, Harvest

class GardenerForm(ModelForm):
    garden = ModelChoiceField(queryset=Garden.objects.all(), widget=HiddenInput())

    class Meta:
        model = Gardener
        exclude = ('added_by', 'updated_by')

class HarvestForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(),
                              widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(HarvestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Harvest
        exclude = ('added',)
        widgets = {
            'area': TextInput(attrs={'size': 5, 'maxlength': 5}),
            'plants': TextInput(attrs={'size': 5, 'maxlength': 5}),
            'harvested': DateInput(format='%m/%d/%Y'),
        }

class MobileHarvestForm(HarvestForm):
    gardener = ModelChoiceField(
        queryset=Gardener.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super(MobileHarvestForm, self).__init__(*args, **kwargs)

        try:
            self._init_gardener(**kwargs)
        except Exception:
            pass

    def _init_gardener(self, **form_kwargs):
        """
        Set the Gardeners that can be chosen, the initially chosen one.
        """
        # get gardeners at this garden
        gardeners = Gardener.objects.filter(
            garden=form_kwargs['initial']['garden']
        ).order_by('name')
        self.fields['gardener'].queryset = gardeners

        # set the initial gardener, using initial kwarg 
        initial_gardener = form_kwargs['initial']['gardener']
        if not initial_gardener or initial_gardener not in gardeners:
            initial_gardener = None
            try:
                # if no gardener in initial kwarg, try to make this user the 
                # initially selected gardener
                gardener = form_kwargs['user'].get_profile().gardener
                if gardener in gardeners:
                    initial_gardener = gardener
            except ObjectDoesNotExist:
                pass

        # finally, if there's only one gardener, select that
        if not initial_gardener and gardeners.count() == 1:
            initial_gardener = gardeners[0]
   
        self.fields['gardener'].initial = initial_gardener

class AutocompleteHarvestForm(HarvestForm):
    gardener = AutoCompleteSelectField('gardener', 
        label="Gardener", 
        required=False,
    )
    variety = AutoCompleteSelectField('variety',
        label='Plant type',
        required=False
    )

    def clean_gardener(self):
        gardener = self.cleaned_data['gardener']
        gardener_name = self.data['gardener_text']

        if not gardener or gardener.name != gardener_name:
            if gardener_name:
                garden = Garden.objects.get(pk=self.data['garden'])
                gardener = get_gardener(gardener_name, garden, self.user)
            else:
                raise ValidationError('Please enter a gardener.')

        return gardener

    def clean_variety(self):
        """
        Clean the variety field. It is an AutoCompleteSelectField, but if a user enters a variety that doesn't exist we try to accomodate it.

        XXX if there is another error on the form, the variety is added but not shown when the form reloads. Ideally, a custom widget would be used instead.
        """
        variety = self.cleaned_data['variety']

        if not variety:
            variety_name = self.data['variety_text']
            if variety_name:
                variety, created = get_variety(variety_name, self.user)
            else:
                raise ValidationError('Please enter a plant type.')

        return variety

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
