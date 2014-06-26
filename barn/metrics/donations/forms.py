from ..forms import RecordForm, RecordedField
from .models import Donation


class DonationForm(RecordForm):
    recorded = RecordedField(label='Date')

    class Meta:
        model = Donation
        fields = ('produce_name', 'pounds', 'recorded', 'added_by', 'garden',)
