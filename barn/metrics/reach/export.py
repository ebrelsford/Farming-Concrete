from django_tablib import Field, ModelDataset

from api.export import PublicMetricDatasetMixin
from ..export import MetricDatasetMixin
from .models import ProgramReach


class ProgramReachDatasetMixin(object):
    recorded_start = Field(header='recorded start')
    recorded = Field(header='recorded end')
    hours_each_day = Field(header='hours each day')
    collaborated_with_organization = Field(header='collaborated with organization')
    collaboration_first = Field(header='first collaboration with organization')
    age_10 = Field(header='# under 10')
    age_10_14 = Field(header='# 10 to 14')
    age_15_19 = Field(header='# 15 to 19')
    age_20_24 = Field(header='# 20 to 24')
    age_25_34 = Field(header='# 25 to 34')
    age_35_44 = Field(header='# 35 to 44')
    age_45_54 = Field(header='# 45 to 54')
    age_55_64 = Field(header='# 55 to 64')
    age_65 = Field(header='# 65 and older')
    gender_male = Field(header='# male')
    gender_female = Field(header='# female')
    gender_other = Field(header='# other gender')
    zipcode_inside = Field(header='# within garden zipcode')
    zipcode_outside = Field(header='# outside garden zipcode')
    other_features = Field(header='other features')

    def __init__(self, *args, **kwargs):
        # Add features_display
        self.base_fields['features_display'] = Field(header='features')
        self._meta.field_order += ('features_display',)
        super(ProgramReachDatasetMixin, self).__init__(*args, **kwargs)

    class Meta:
        model = ProgramReach
        fields = [
            'recorded_start',
            'recorded',
            'hours_each_day',
            'collaborated_with_organization',
            'collaboration_first',
            'age_10',
            'age_10_14',
            'age_15_19',
            'age_20_24',
            'age_25_34',
            'age_35_44',
            'age_45_54',
            'age_55_64',
            'age_65',
            'gender_male',
            'gender_female',
            'gender_other',
            'zipcode_inside',
            'zipcode_outside',
            'other_features',
        ]
        field_order = (
            'recorded_start',
            'recorded',
            'hours_each_day',
            'collaborated_with_organization',
            'collaboration_first',
            'age_10',
            'age_10_14',
            'age_15_19',
            'age_20_24',
            'age_25_34',
            'age_35_44',
            'age_45_54',
            'age_55_64',
            'age_65',
            'gender_male',
            'gender_female',
            'gender_other',
            'zipcode_inside',
            'zipcode_outside',
            'other_features',
        )


class ProgramReachDataset(ProgramReachDatasetMixin, MetricDatasetMixin,
                          ModelDataset):

    def __init__(self, *args, **kwargs):
        # Add name
        self.base_fields['name'] = Field(header='name')
        self._meta.field_order += ('name',)

        super(ProgramReachDataset, self).__init__(*args, **kwargs)


class PublicProgramReachDataset(ProgramReachDatasetMixin,
                                PublicMetricDatasetMixin, ModelDataset):
    pass
