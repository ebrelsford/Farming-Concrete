from django.db import models
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditedModel


class BaseMetricRecord(AuditedModel):
    """
    The base model for a data entry point for a metric.
    """

    garden = models.ForeignKey('farmingconcrete.Garden',
        blank=True,
        null=True,
        help_text=_('The garden this refers to'),
        verbose_name=_('garden'),
    )

    recorded = models.DateField(_('recorded'),
        blank=True,
        null=True,
        help_text=_('The date this was recorded'),
    )

    class Meta:
        abstract = True
