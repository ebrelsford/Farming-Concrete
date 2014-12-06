from django.db import models
from django.db.models import Count, Max, Min
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from audit.models import AuditedModel


class MetricQuerySet(QuerySet):
    public_dict_values_args = ('garden__pk', 'recorded',)

    def after(self, start):
        return self.filter(recorded__gte=start)

    def before(self, end):
        return self.filter(recorded__lte=end)

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

    def garden_pks(self):
        return self.values_list('garden', flat=True).distinct()

    def added_by_pks(self):
        return self.values_list('added_by', flat=True).distinct()

    def public_dict(self):
        """
        Get a dict of this queryset that is JSON-serializable.

        Garden PKs will need to be anonymized elsewhere to safely share 
        publicly.
        """
        return self.values(self.public_dict_values_args)


class MetricManager(models.Manager):

    def get_queryset(self):
        return MetricQuerySet(self.model)

    def after(self, start):
        return self.get_queryset().after(start)

    def before(self, end):
        return self.get_queryset().before(end)

    def for_dates(self, start, end):
        return self.get_queryset().for_dates(start, end)

    def for_garden(self, garden):
        return self.get_queryset().for_garden(garden)

    def for_gardens(self, gardens):
        return self.get_queryset().for_gardens(gardens)

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

    def _added_by_display(self):
        u = self.added_by
        if not u:
            return ''
        if u.first_name:
            if u.last_name:
                return '%s %s.' % (u.first_name, u.last_name[0])
            return u.first_name
        return u.username
    added_by_display = property(_added_by_display)

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
    def get_records(cls, gardens=None, year=None, start=None, end=None):
        """
        Get the records for this metric for the given garden and dates.
        """
        records = cls.objects.all()
        if gardens:
            if not isinstance(gardens, (list, tuple)):
                gardens = (gardens,)
            records = cls.objects.for_gardens(gardens)
        if year:
            records = records.for_year(year)
        elif start and end:
            records = records.for_dates(start, end)
        elif start:
            records = records.after(start)
        elif end:
            records = records.before(end)
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
        return cls.summarize(cls.get_records(gardens=gardens, **kwargs))
