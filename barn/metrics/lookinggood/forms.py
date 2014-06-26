from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from ..forms import RecordedField, RecordForm
from .models import LookingGoodEvent, LookingGoodItem, LookingGoodPhoto


class LookingGoodPhotoForm(ModelForm):

    class Meta:
        model = LookingGoodPhoto


LookingGoodPhotoFormSet = inlineformset_factory(LookingGoodEvent, LookingGoodPhoto,
    can_delete=False,
    extra=1,
    form=LookingGoodPhotoForm,
)


class LookingGoodItemForm(ModelForm):

    class Meta:
        model = LookingGoodItem


LookingGoodItemFormSet = inlineformset_factory(LookingGoodEvent, LookingGoodItem,
    can_delete=False,
    extra=1,
    form=LookingGoodItemForm,
)


class LookingGoodEventForm(RecordForm):
    recorded = RecordedField(label='Event date')

    class Meta:
        model = LookingGoodEvent
        fields = ('recorded', 'total_tags', 'total_participants',
                  'items_tagged', 'added_by', 'garden',)
