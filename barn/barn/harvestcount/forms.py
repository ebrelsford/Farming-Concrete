from django.forms import ModelForm, HiddenInput, ModelChoiceField, TextInput, CharField, DecimalField, DateInput, ValidationError

from ajax_select.fields import AutoCompleteSelectField

from farmingconcrete.models import Garden, Variety
from models import Gardener, Harvest

class HarvestForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(), widget=HiddenInput())
    gardener = AutoCompleteSelectField('gardener', 
        label="Gardener", 
        required=False,
        error_messages={
            'required': "Please enter a gardener.",
        }
    )
    variety = AutoCompleteSelectField('variety',
        label='Plant type',
        required=False
    )

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

    def clean_gardener(self):
        gardener = self.cleaned_data['gardener']

        if not gardener:
            gardener_name = self.data['gardener_text']
            if gardener_name:
                garden = Garden.objects.get(pk=self.data['garden'])
                gardener = Gardener(name=gardener_name, garden=garden, added_by=self.user)
                gardener.save()
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
                moderated = not self.user.has_perm('farmingconcrete.add_variety_unmoderated')
                variety = Variety(name=variety_name, added_by=self.user, needs_moderation=moderated)
                variety.save()
            else:
                raise ValidationError('Please enter a plant type.')

        return variety
