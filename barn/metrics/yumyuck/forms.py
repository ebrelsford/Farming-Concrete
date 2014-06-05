from django.forms import ModelChoiceField

from crops.forms import AddNewCropWidget
from crops.models import Crop

from ..forms import RecordedField, RecordForm
from .models import YumYuck


class YumYuckForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )
    crop = ModelChoiceField(
        label='Crop name',
        queryset=Crop.objects.filter(needs_moderation=False),
        widget=AddNewCropWidget(),
    )

    class Meta:
        model = YumYuck
        fields = ('recorded', 'crop', 'yum_before', 'yuck_before',
                  'yum_after', 'yuck_after', 'added_by', 'garden',)
