from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

from ..forms import RecordedField, RecordForm
from .models import ProgramFeature, ProgramReach


class ProgramReachForm(RecordForm):
    recorded_start = RecordedField(
        label=_('Program start'),
        required=True,
    )
    recorded = RecordedField(
        label=_('Program end'),
        required=True,
    )

    features = ModelMultipleChoiceField(
        queryset = ProgramFeature.objects.filter(universal=True),
        widget = CheckboxSelectMultiple(),
    )

    class Meta:
        model = ProgramReach
        fields = ('name', 'recorded_start', 'recorded', 'hours_each_day',
                  'collaborated_with_organization', 'collaboration_first',
                  'age_10', 'age_10_14', 'age_15_19', 'age_20_24', 'age_25_34',
                  'age_35_44', 'age_45_54', 'age_55_64', 'age_65',
                  'gender_male', 'gender_female', 'gender_other',
                  'zipcode_inside', 'zipcode_outside', 'features', 'added_by',
                  'garden',)
