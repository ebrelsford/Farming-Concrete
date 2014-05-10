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

    def for_gardens(self, gardens):
        return self.filter(garden__pk__in=[garden.pk for garden in gardens])

    def for_year(self, year):
        return self.filter(recorded__year=year)

    def year_range(self):
        date_range = self.aggregate(Min('recorded'), Max('recorded'))
        return (
            date_range['recorded__min'].year,
            date_range['recorded__max'].year,
        )


class MetricManager(models.Manager):

    def get_query_set(self):
        return MetricQuerySet(self.model)

    def for_dates(self, start, end):
        return self.get_query_set().for_dates(start, end)

    def for_garden(self, garden):
        return self.get_query_set().for_garden(garden)

    def for_gardens(self, gardens):
        return self.get_query_set().for_gardens(gardens)

    def for_year(self, year):
        return self.get_query_set().for_year(year)


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
    def get_records(cls, gardens, year=None, start=None, end=None):
        """
        Get the records for this metric for the given garden and dates.
        """
        if not isinstance(gardens, (list, tuple)):
            gardens = (gardens,)
        records = cls.objects.for_gardens(gardens)
        if year:
            records = records.for_year(year)
        elif start and end:
            records = records.for_dates(start, end)
        return records

    @classmethod
    def get_summary_data(cls, gardens, **kwargs):
        """
        Get a summary of this metric for the given garden and dates.
        """
        if isinstance(gardens, QuerySet):
            gardens = list(gardens)
        if gardens and not isinstance(gardens, (list, tuple)):
            gardens = (gardens,)
        return cls.summarize(cls.get_records(gardens, **kwargs))
