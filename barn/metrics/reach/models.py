from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord
from ..registry import register


class ProgramFeature(models.Model):
    name = models.CharField(_('name'),
        max_length=300,
    )

    universal = models.BooleanField(_('universal'),
        default=True,
        help_text=_('This feature should be available to all gardens'),
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProgramReach(BaseMetricRecord):

    name = models.CharField(_('program name'),
        max_length=300,
        help_text=_('The name of the program'),
    )

    recorded_start = models.DateField(_('program start'),
        help_text=_('When this program started'),
    )

    hours_each_day = models.DecimalField(_('hours each day'),
        max_digits=3,
        decimal_places=1,
        help_text=_('The number of hours each day the program ran'),
    )

    collaborated_with_organization = models.BooleanField(
        _('collaborated with organization'),
        default=False,
        help_text=_('Did you collaborate with another organization to host '
                    'this program?'),
    )

    collaboration_first = models.BooleanField(_('first collaboration'),
        default=False,
        help_text=_('If you did collaborate with another organization, was '
                    'this the first time you worked together?'),
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

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(ProgramReach, cls).get_summarize_kwargs()
        kwargs.update({
            'hours_each_day': Sum('hours_each_day'),
            'age_10': Sum('age_10'),
        })
        return kwargs


register('Reach of Programs', {
    'all_gardens_url_name': 'reach_program_all_gardens',
    'model': ProgramReach,
    'number': 5,
    'garden_detail_url_name': 'reach_program_garden_details',
    'group': 'Social Data',
    'group_number': 2,
    'index_url_name': 'reach_program_index',
    'summarize_template': 'metrics/reach/program/summarize.html',
    'user_gardens_url_name': 'reach_program_user_gardens',
})
