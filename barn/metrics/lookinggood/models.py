from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from ..models import BaseMetricRecord, MetricManager, MetricQuerySet


class LookingGoodEventQuerySet(MetricQuerySet):

    def public_dict(self):
        values_args = self.public_dict_values_args + (
            'total_participants',
            'total_tags',
            'items_tagged',
        )
        return self.values(*values_args)


class LookingGoodEventManager(MetricManager):
    
    def get_queryset(self):
        return LookingGoodEventQuerySet(self.model)


class LookingGoodPhoto(models.Model):
    event = models.ForeignKey('LookingGoodEvent',
        verbose_name=_('event')
    )

    photo = models.ImageField(_('photo'),
        upload_to='lookinggood_event',
        blank=True,
        null=True,
    )
    caption = models.CharField(_('caption'),
        max_length=250,
        blank=True,
        null=True,
    )


class LookingGoodItem(models.Model):
    event = models.ForeignKey('LookingGoodEvent',
        verbose_name=_('event')
    )

    name = models.CharField(_('Tagged item'),
        max_length=150,
    )
    tags = models.PositiveIntegerField(_('# of tags'))
    comments = models.TextField(_('Comments'))


class LookingGoodEvent(BaseMetricRecord):
    objects = LookingGoodEventManager()
    total_participants = models.PositiveIntegerField(_('# of participants'),
        default=0,
    )
    total_tags = models.PositiveIntegerField(_('# of tags'),
        default=0,
    )
    items_tagged = models.PositiveIntegerField(_('# of items tagged'),
        default=0,
    )

    def __unicode__(self):
        return "%d looking good tags" % (self.total_tags,)

    @classmethod
    def get_summarize_kwargs(cls):
        kwargs = super(LookingGoodEvent, cls).get_summarize_kwargs()
        kwargs.update({
            'total_tags': Sum('total_tags'),
        })
        return kwargs
