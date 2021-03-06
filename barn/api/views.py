from collections import OrderedDict
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
from units.convert import to_weight_units


def get_random_id():
    return str(uuid4()).split('-')[0]


class DecimalJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalJSONEncoder, self).default(o)


class AvailableFiltersView(JSONResponseMixin, View):
    # TODO cache

    def get_cities(self, state):
        cities = list(set(Garden.objects.filter(state=state).values_list('city', flat=True)))
        return sorted(filter(None, cities))

    def get_groups(self):
        groups = list(set(Garden.objects.values_list('gardengroup__name', flat=True)))
        return sorted(filter(None, groups))

    def get_metrics(self):
        metrics_grouped = registry.by_group()
        new_metrics = OrderedDict()
        for name, metrics in metrics_grouped.items():
            new_metrics[name] = [m['name'] for m in metrics]
        return new_metrics

    def get_states(self):
        states = list(set(Garden.objects.values_list('state', flat=True)))
        return sorted(filter(None, states))

    def get_zips(self, state):
        zips = list(set(Garden.objects.filter(state=state).values_list('zip', flat=True)))
        return sorted(filter(None, zips))

    def get_types(self):
        types = list(set(Garden.objects.values_list('type__name', flat=True)))
        return sorted(filter(None, types))

    def get(self, request, *args, **kwargs):
        states_dict = OrderedDict()
        for state in self.get_states():
            states_dict[state] = {
                'cities': self.get_cities(state),
                'zips': self.get_zips(state),
            }
        return self.render_json_response({
            'garden_types': self.get_types(),
            'groups': self.get_groups(),
            'metrics': self.get_metrics(),
            'states': states_dict,
        })


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
        metrics = GET.getlist('metric')
        if len(metrics) == 1 and metrics[0] == '':
            metrics = None
        filters = {
            # Metrics
            'metrics': metrics,

            # Groups
            'groups': GET.getlist('group'),

            # Garden types
            'garden_types': GET.getlist('garden_type'),
        }

        # Where
        filters.update(dict([(k, GET.get(k, None)) for k in self.where_fields]))

        # When
        filters.update(dict([(k, self.parse_date(GET.get(k, None))) for k 
                             in self.when_fields]))

        return filters

    def get_queryset_filters(self, request):
        filters = self.filters(request)

        def explode_filters(city=None, state=None, zip=None, groups=None,
                            garden_types=None, start=None, end=None, **kwargs):
            garden_filters = Q()
            if city:
                # If searching in all boroughs, require borough
                if city == 'All boroughs':
                    garden_filters = garden_filters & Q(garden__borough__isnull=False)
                else:
                    garden_filters = garden_filters & Q(Q(garden__city=city) |
                                                        Q(garden__borough=city))
            if state:
                garden_filters = garden_filters & Q(garden__state=state)
            if zip:
                garden_filters = garden_filters & Q(garden__zip=zip)
            if groups:
                garden_filters = garden_filters & Q(garden__gardengroup__name__in=groups)
            if garden_types:
                garden_filters = garden_filters & Q(garden__type__name__in=garden_types)

            when_filters = Q()
            if start:
                when_filters = when_filters & Q(recorded__gte=start)
            if end:
                when_filters = when_filters & Q(recorded__lte=end)
            return Q(garden_filters & when_filters)

        return explode_filters(**filters)

    def get_metrics(self, metrics=None, **kwargs):
        return registry.sorted(metrics=metrics)


class OverviewView(JSONResponseMixin, View):

    def get_cities(self):
        cities = Garden.objects.filter(
            has_metric_records=True,
            city__isnull=False
        ).exclude(city='').values_list( 'city', 'state').distinct()
        return len(cities)

    def get_compost_pounds(self):
        grams = CompostProductionWeight.objects.aggregate(grams=Sum('weight'))['grams']
        return round(to_weight_units(grams, 'imperial').magnitude)

    def get_food_pounds(self):
        grams = Harvest.objects.aggregate(grams=Sum('weight'))['grams']
        return round(to_weight_units(grams, 'imperial').magnitude)

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'cities': self.get_cities(),
            'gardens': Garden.objects.filter(has_metric_records=True).count(),
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
                    "records": [*],
                    "chart": {
                        "y": "<header_name>",
                        "title": "<title>"
                    }
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

        records = metric['model'].objects \
                .filter(self.get_queryset_filters(self.request)) \
                .order_by('recorded') \
                .public_dict()
        return self._records_combine_units(records)

    def _records_combine_units(self, records):
        """Include units of measurement for measurements."""
        for record in records:
            for k, v in record.items():
                if k.endswith('_units'):
                    mag_key = k.replace('_units', '')
                    if mag_key in record:
                        record[mag_key] = {
                            'magnitude': record[mag_key],
                            'units': v,
                        }
                        del record[k]
        return records

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

    def get_metric_headers(self, metric):
        fields = metric._meta.fields
        return dict([(f.name, f.verbose_name.lower()) for f in fields])

    def get_results(self, **filters):
        metrics = self.get_metrics(**filters)
        metric_entries = []
        for metric in metrics:
            metric_entries.append({
                'group_number': metric['group_number'],
                'headers': self.get_metric_headers(metric['model']),
                'name': metric['name'],
                'number': metric['number'],
                'records': list(self.get_records(metric=metric, **filters)),
                'chart': metric.get('chart', {}),
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

            ds = dataset_cls(filters=self.get_queryset_filters(self.request),
                             measurement_system='imperial')

            # Replace garden column with a randomized unique id
            try:
                index = ds.headers.index('garden')
                ds.insert_col(index,
                              lambda r: obfuscated_garden(garden_mapping, r, index), 
                              header='garden unique id')
                del ds['garden']
            except IndexError:
                # Ignore case where garden column not present
                pass

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
