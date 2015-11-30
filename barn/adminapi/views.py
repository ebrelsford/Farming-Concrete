import geojson

from django.db.models import Count

from actstream.models import Action
from django_filters import FilterSet, DateFilter, MultipleChoiceFilter
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import ActionSerializer


class ActionFilter(FilterSet):
    min_timestamp = DateFilter(name='timestamp', lookup_type='gte')
    max_timestamp = DateFilter(name='timestamp', lookup_type='lte')
    verb = MultipleChoiceFilter(choices=(
        ('added garden', 'added garden'),
        ('added garden group', 'added garden group'),
        ('downloaded garden group spreadsheet', 'downloaded garden group spreadsheet'),
        ('downloaded garden report', 'downloaded garden report'),
        ('downloaded garden spreadsheet', 'downloaded garden spreadsheet'),
        ('joined Farming Concrete', 'joined Farming Concrete'),
        ('recorded', 'recorded'),
    ))

    class Meta:
        model = Action
        fields = ['timestamp', 'verb',]


class ActionsViewset(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ActionFilter
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all().order_by('-timestamp')
    serializer_class = ActionSerializer


class ActionsSummaryView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ActionFilter
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get count of actions by month
        counts = queryset.extra(select={
            'month': 'EXTRACT(month FROM timestamp)',
            'year': 'EXTRACT(year from timestamp)',
        }) \
                .values('month', 'year') \
                .order_by('year', 'month') \
                .annotate(count=Count('timestamp'))

        return Response({
            'counts': counts,
        })


class ActionsGeojsonView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ActionFilter
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        features = self.get_features(queryset)
        return Response(geojson.FeatureCollection(features))

    def get_features(self, queryset):
        for action in queryset.all():
            try:
                coordinates = [
                    action.action_object.longitude,
                    action.action_object.latitude,
                ]
            except AttributeError:
                try:
                    coordinates = [
                        action.target.longitude,
                        action.target.latitude,
                    ]
                except AttributeError:
                    continue

            yield geojson.Feature(
                id=action.pk,
                geometry=geojson.Point(coordinates=coordinates)
            )
