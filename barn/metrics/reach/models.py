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

    age_10 = models.IntegerField(_('Participants under 10'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were under age 10'),
    )

    age_10_14 = models.IntegerField(_('Participants between 10 and 14'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 10 and '
                    '14'),
    )

    age_15_19 = models.IntegerField(_('Participants between 15 and 19'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 15 and '
                    '19'),
    )

    age_20_24 = models.IntegerField(_('Participants between 20 and 24'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 20 and '
                    '24'),
    )

    age_25_34 = models.IntegerField(_('Participants between 25 and 34'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 25 and '
                    '34'),
    )

    age_35_44 = models.IntegerField(_('Participants between 35 and 44'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 35 and '
                    '44'),
    )

    age_45_54 = models.IntegerField(_('Participants between 45 and 54'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 45 and '
                    '54'),
    )

    age_55_64 = models.IntegerField(_('Participants between 55 and 64'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were between ages 55 and '
                    '64'),
    )

    age_65 = models.IntegerField(_('Participants 65 and older'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were 65 and older'),
    )

    gender_male = models.IntegerField(_('Participants male'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were male'),
    )

    gender_female = models.IntegerField(_('Participants female'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were female'),
    )

    gender_other = models.IntegerField(_('Participants other gender'),
        blank=True,
        null=True,
        help_text=_('The number of participants who were another gender'),
    )

    zipcode_inside = models.IntegerField(
        _('Participants within garden zip code'),
        blank=True,
        null=True,
        help_text=_("The number of participants who live within the garden's "
                    "zip code"),
    )

    zipcode_outside = models.IntegerField(
        _('Participants outside garden zip code'),
        blank=True,
        null=True,
        help_text=_("The number of participants who live outside the garden's "
                    "zip code"),
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


register('Program Reach', {
    'all_gardens_url_name': 'reach_program_all_gardens',
    'model': ProgramReach,
    'garden_detail_url_name': 'reach_program_garden_details',
    'group': 'Skills & Knowledge',
    'index_url_name': 'reach_program_index',
    'summarize_template': 'metrics/reach/program/summarize.html',
    'user_gardens_url_name': 'reach_program_user_gardens',
})
