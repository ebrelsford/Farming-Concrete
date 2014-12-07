from datetime import date, datetime
import decimal
from uuid import uuid4

from tablib import Databook

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, Q
from django.http import Http404
from django.views.generic import View

from braces.views import JSONResponseMixin

from farmingconcrete.models import Garden
from generic.views import TablibView
from metrics.compost.models import CompostProductionWeight
from metrics.harvestcount.models import Harvest
from metrics.registry import registry


def get_random_id():
    return str(uuid4()).split('-')[0]


class DecimalJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalJSONEncoder, self).default(o)


class FilteredApiMixin(object):
    date_format = '%m/%d/%y'
    where_fields = ('state', 'city', 'zip',)
    when_fields = ('start', 'end',)

    def parse_date(self, date):
        try:
            return datetime.strptime(date, self.date_format)
        except Exception:
            return None

    def filters(self, request):
        """Get filters from the request"""
        GET = request.GET
        return {
            # Metrics
            'metrics': GET.getlist('metric'),

            # Where
            'where': dict([(k, GET.get(k, None)) for k in self.where_fields]),

            # When
            'when': dict([(k, self.parse_date(GET.get(k, None))) for k in \
                          self.when_fields]),

            # Groups
            'groups': GET.getlist('group'),

            # Garden types
            'garden_types': GET.getlist('garden_type'),
        }

    def get_metrics(self, metrics=None, **kwargs):
        return registry.sorted(metrics=metrics)


class OverviewView(JSONResponseMixin, View):

    def get_compost_pounds(self):
        pounds = CompostProductionWeight.objects.aggregate(pounds=Sum('weight'))['pounds']
        return round(pounds)

    def get_food_pounds(self):
        pounds = Harvest.objects.aggregate(pounds=Sum('weight'))['pounds']
        return round(pounds)

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'gardens': Garden.objects.count(),
            'pounds_of_compost': self.get_compost_pounds(),
            'pounds_of_food': self.get_food_pounds(),
        })


class RecordsView(FilteredApiMixin, JSONResponseMixin, View):
    """
    Get records, filtered, structured like this:

    {
        "results": {
            "gardens": {
                "count": 5
            }
            "metrics": [
                {
                    "name": "<metric name>",
                    "records": [*]
                }
            ]
        }
    }
    """
    json_encoder_class = DecimalJSONEncoder

    def get_records(self, metric=None, city=None, state=None, zip=None,
                    groups=None, garden_types=None, start=None, end=None,
                    **filters):
        if not metric:
            return []

        garden_filters = Q()
        if city:
            # TODO if city OR borough OR "all NYC" -> all boroughs
            garden_filters = garden_filters & Q(Q(garden__city=city) |
                                                Q(garden__borough=city))
        if state:
            garden_filters = garden_filters & Q(garden__state=state)
        if zip:
            garden_filters = garden_filters & Q(garden__zip=zip)
        if groups:
            garden_filters = garden_filters & Q(garden__gardengroup__in=groups)
        if garden_types:
            garden_filters = garden_filters & Q(garden__type__in=garden_types)

        when_filters = Q()
        if start:
            when_filters & Q(recorded__gte=start)
        if end:
            when_filters & Q(recorded__lte=end)

        return metric['model'].objects.filter(garden_filters, when_filters) \
                .order_by('recorded') \
                .public_dict()

    def anonymize(self, metric_entries):
        """
        Remove garden keys from output entries since they can easily be tied
        back to the gardens.
        """
        garden_ids = {}
        for entry in metric_entries:
            for record in entry['records']:
                try:
                    new_id = garden_ids[record['garden__pk']]
                except KeyError:
                    new_id = garden_ids[record['garden__pk']] = get_random_id()
                record['garden'] = new_id
                del record['garden__pk']
        return metric_entries

    def count_gardens(self, metric_entries):
        gardens = []
        for entry in metric_entries:
            gardens += [r['garden__pk'] for r in entry['records']]
        return len(set(gardens))

    def get_results(self, **filters):
        metrics = self.get_metrics(**filters)
        metric_entries = []
        for metric in metrics:
            metric_entries.append({
                'name': metric['name'],
                'records': list(self.get_records(metric=metric, **filters)),
            })
        return {
            'gardens': {
                'count': self.count_gardens(metric_entries),
            },
            'metrics': self.anonymize(metric_entries),
        }

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'results': self.get_results(**self.filters(request)),
        })


def obfuscated_garden(gardens, row, index):
    garden_id = row[index]
    try:
        return gardens[garden_id]
    except KeyError:
        gardens[garden_id] = get_random_id()
        return gardens[garden_id]


class SpreadsheetView(FilteredApiMixin, TablibView):
    """Export data as an Excel spreadsheet."""
    format = 'xlsx'

    def get(self, request, *args, **kwargs):
        self.request_filters = self.filters(request)
        self.metrics = self.get_metrics(**self.request_filters)
        return super(SpreadsheetView, self).get(request, *args, **kwargs)

    def get_dataset(self):
        datasets = []

        # Mapping of gardens to obfuscated ids, global for each download
        garden_mapping = {}

        for metric in sorted(self.metrics):
            dataset_cls = metric['public_dataset']
            if not dataset_cls:
                continue

            ds = dataset_cls(**self.request_filters)

            # Replace garden column with a randomized unique id
            index = ds.headers.index('garden')
            ds.insert_col(index,
                          lambda r: obfuscated_garden(garden_mapping, r, index), 
                          header='garden unique id')
            del ds['garden']

            # Only append if there is data to append
            if not ds.height:
                continue

            # Sheet titles can be 31 characters at most, cannot contain :s
            ds.title = metric['name'][:31].replace(':', '')
            datasets.append(ds)
        if not datasets:
            raise Http404
        return Databook(datasets)

    def get_filename(self):
        return '%s - %s' % (
            'Mill export',
            date.today().strftime('%Y-%m-%d'),
        )
