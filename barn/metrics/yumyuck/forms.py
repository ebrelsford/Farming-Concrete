from ..forms import RecordedField, RecordForm
from .models import YumYuck


class YumYuckForm(RecordForm):
    recorded = RecordedField(
        required=True,
    )

    class Meta:
        model = YumYuck
        fields = ('recorded', 'vegetable', 'yum_before', 'yuck_before',
                  'yum_after', 'yuck_after', 'added_by', 'garden',)
