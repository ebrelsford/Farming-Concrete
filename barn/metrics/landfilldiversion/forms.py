from ..forms import RecordForm
from .models import LandfillDiversionVolume, LandfillDiversionWeight


class LandfillDiversionWeightForm(RecordForm):

    class Meta:
        model = LandfillDiversionWeight
        fields = ('recorded', 'weight', 'added_by', 'garden',)


class LandfillDiversionVolumeForm(RecordForm):

    class Meta:
        model = LandfillDiversionVolume
        fields = ('recorded', 'volume', 'added_by', 'garden',)
