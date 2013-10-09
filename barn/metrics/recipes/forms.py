from django.utils.translation import ugettext_lazy as _

from ..forms import RecordedField, RecordForm
from .models import RecipeTally


class RecipeTallyForm(RecordForm):
    recorded_start = RecordedField()

    recorded = RecordedField(
        label=_('Recorded end'),
        required=True,
    )

    class Meta:
        model = RecipeTally
        fields = ('recorded_start', 'recorded', 'recipes_count', 'added_by',
                  'garden',)
