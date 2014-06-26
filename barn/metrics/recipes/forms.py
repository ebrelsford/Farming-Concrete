from django.utils.translation import ugettext_lazy as _

from ..forms import RecordedField, RecordForm
from .models import RecipeTally


class RecipeTallyForm(RecordForm):
    recorded_start = RecordedField(label=_('Start date'))
    recorded = RecordedField(label=_('End date'))

    class Meta:
        model = RecipeTally
        fields = ('recorded_start', 'recorded', 'recipes_count', 'added_by',
                  'garden',)
