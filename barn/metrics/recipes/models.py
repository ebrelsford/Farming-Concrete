from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class RecipeTallyQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'recipes_count',
            'recorded_start',
        )
        return self.values(*values_args)


class RecipeTallyManager(MetricManager):
    
    def get_queryset(self):
        return RecipeTallyQuerySet(self.model)


class RecipeTally(BaseMetricRecord):
    objects = RecipeTallyManager()
    recorded_start = models.DateField(_('recorded start'))
    recipes_count = models.PositiveIntegerField(_('# of recipes'))

    def __unicode__(self):
        return '%d recipes' % (self.recipes_count,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(RecipeTally, cls).get_summarize_kwargs()
        kwargs.update({
            'recipes_count': Sum('recipes_count'),
        })
        return kwargs
