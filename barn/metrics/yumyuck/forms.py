from django.forms import ModelChoiceField

from farmingconcrete.forms import AddNewVarietyWidget
from farmingconcrete.models import Variety

from ..forms import RecordedField, RecordForm
from .models import YumYuck


class YumYuckForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )
    vegetable = ModelChoiceField(
        # TODO move to crops.Crop / crops.Variety
        queryset=Variety.objects.filter(needs_moderation=False),
        widget=AddNewVarietyWidget(),
    )

    class Meta:
        model = YumYuck
        fields = ('recorded', 'vegetable', 'yum_before', 'yuck_before',
                  'yum_after', 'yuck_after', 'added_by', 'garden',)
