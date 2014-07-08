from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class ProgramFeature(models.Model):
    name = models.CharField(_('name'),
        max_length=300,
    )
    order = models.PositiveIntegerField(default=0)

    universal = models.BooleanField(_('universal'),
        default=True,
        help_text=_('This feature should be available to all gardens'),
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order',)


class ProgramReach(BaseMetricRecord):

    name = models.CharField(_('program name'),
        max_length=300,
    )

    recorded_start = models.DateField(_('program start'))

    hours_each_day = models.DecimalField(_('hours each day'),
        max_digits=3,
        decimal_places=1,
    )

    collaborated_with_organization = models.BooleanField(
        _('Did you collaborate with another organization to host this program?'),
        default=False,
    )

    collaboration_first = models.BooleanField(
        _('Was this the first time you worked together?'),
        default=False,
    )

    age_10 = models.IntegerField(_('# Under 10'),
        blank=True,
        null=True,
    )

    age_10_14 = models.IntegerField(_('# 10 to 14'),
        blank=True,
        null=True,
    )

    age_15_19 = models.IntegerField(_('# 15 to 19'),
        blank=True,
        null=True,
    )

    age_20_24 = models.IntegerField(_('# 20 to 24'),
        blank=True,
        null=True,
    )

    age_25_34 = models.IntegerField(_('# 25 to 34'),
        blank=True,
        null=True,
    )

    age_35_44 = models.IntegerField(_('# 35 to 44'),
        blank=True,
        null=True,
    )

    age_45_54 = models.IntegerField(_('# 45 to 54'),
        blank=True,
        null=True,
    )

    age_55_64 = models.IntegerField(_('# 55 to 64'),
        blank=True,
        null=True,
    )

    age_65 = models.IntegerField(_('65 and older'),
        blank=True,
        null=True,
    )

    gender_male = models.IntegerField(_('# Male'),
        blank=True,
        null=True,
    )

    gender_female = models.IntegerField(_('# Female'),
        blank=True,
        null=True,
    )

    gender_other = models.IntegerField(_('# Other gender'),
        blank=True,
        null=True,
    )

    zipcode_inside = models.IntegerField(_('# Within garden zip code'),
        blank=True,
        null=True,
    )

    zipcode_outside = models.IntegerField(_('# Outside garden zip code'),
        blank=True,
        null=True,
    )

    features = models.ManyToManyField('ProgramFeature',
        blank=True,
        null=True,
        help_text=_('Features this program included'),
        verbose_name=_('features'),
    )
    other_features = models.CharField(_('other features'),
        max_length=200,
        blank=True,
        null=True,
    )

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(ProgramReach, cls).get_summarize_kwargs()
        kwargs.update({
            'programs': Count('pk'),
            'hours_each_day': Sum('hours_each_day'),
            'age_10': Sum('age_10'),
        })
        return kwargs


register('Reach of Programs', {
    'all_gardens_url_name': 'reach_program_all_gardens',
    'download_url_name': 'reach_program_garden_csv',
    'model': ProgramReach,
    'number': 5,
    'garden_detail_url_name': 'reach_program_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'reach_program_index',
    'short_name': 'program',
})
