from django.forms import IntegerField, ModelChoiceField

from crops.forms import AddNewCropWidget
from crops.models import Crop

from ..forms import RecordedField, RecordForm
from .models import YumYuck


class YumYuckForm(RecordForm):
    recorded = RecordedField(label='Event date')
    crop = ModelChoiceField(
        label='Crop name',
        queryset=Crop.objects.filter(needs_moderation=False),
        widget=AddNewCropWidget(),
    )
    yum_before = IntegerField(label='Yums')
    yuck_before = IntegerField(label='Yucks')
    yum_after = IntegerField(label='Yums')
    yuck_after = IntegerField(label='Yucks')

    class Meta:
        model = YumYuck
        fields = ('recorded', 'crop', 'yum_before', 'yuck_before',
                  'yum_after', 'yuck_after', 'added_by', 'garden',)
