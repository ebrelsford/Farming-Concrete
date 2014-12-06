import decimal
from uuid import uuid4

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.views.generic import View

from braces.views import JSONResponseMixin

from metrics.registry import registry


class DecimalJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalJSONEncoder, self).default(o)


class FilteredApiMixin(object):
    where_fields = ('state', 'city', 'zip',)
    when_fields = ('start', 'end',)

    def filters(self, request):
        """Get filters from the request"""
        GET = request.GET
        return {
            # Metrics
            'metrics': GET.getlist('metric'),

            # Where
            'where': dict([(k, GET.get(k, None)) for k in self.where_fields]),

            # When
            'when': dict([(k, GET.get(k, None)) for k in self.when_fields]),

            # Groups
            'groups': GET.getlist('group'),

            # Garden types
            'garden_types': GET.getlist('garden_type'),
        }

    def get_metrics(self, metrics=None, **kwargs):
        return registry.sorted(metrics=metrics)


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
                    new_id = garden_ids[record['garden__pk']] = str(uuid4()).split('-')[0]
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
