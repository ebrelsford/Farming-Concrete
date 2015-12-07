from ..forms import RecordForm
from .models import CompostProductionVolume, CompostProductionWeight


class CompostProductionWeightForm(RecordForm):

    class Meta(RecordForm.Meta):
        model = CompostProductionWeight
        fields = ('recorded', 'weight_new', 'added_by', 'garden',)


class CompostProductionVolumeForm(RecordForm):

    class Meta:
        model = CompostProductionVolume
        fields = ('recorded', 'volume', 'added_by', 'garden',)
