from django.db import models
from django.db.models import Count, Max, Min
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditedModel


class MetricQuerySet(QuerySet):

    def for_dates(self, start, end):
        return self.filter(recorded__gte=start, recorded__lte=end)

    def for_garden(self, garden):
        return self.filter(garden=garden)

    def for_year(self, year):
        return self.filter(recorded__year=year)


class MetricManager(models.Manager):

    def get_queryset(self):
        return MetricQuerySet(self.model)

    def for_dates(self, start, end):
        return self.get_queryset().for_dates(start, end)

    def for_garden(self, garden):
        return self.get_queryset().for_garden(garden)

    def for_year(self, year):
        return self.get_queryset().for_year(year)


class BaseMetricRecord(AuditedModel):
    """
    The base model for a data entry point for a metric.
    """

    objects = MetricManager()

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

    @classmethod
    def summarize(cls, records):
        """
        Summarize the given records in a way that will make sense in a template
        context.
        """
        if not records:
            return None
        return records.aggregate(**cls.get_summarize_kwargs())

    @classmethod
    def get_summarize_kwargs(cls):
        return {
            'count': Count('pk'),
            'gardens': Count('garden__pk', distinct=True),
            'recorded_min': Min('recorded'),
            'recorded_max': Max('recorded'),
        }

    @classmethod
    def get_records(cls, garden, year=None, start=None, end=None):
        """
        Get the records for this metric for the given garden and dates.
        """
        records = cls.objects.for_garden(garden)
        if year:
            records = records.for_year(year)
        elif start and end:
            records = records.for_dates(start, end)
        return records

    @classmethod
    def get_summary_data(cls, garden, **kwargs):
        """
        Get a summary of this metric for the given garden and dates.
        """
        return cls.summarize(cls.get_records(garden, **kwargs))
