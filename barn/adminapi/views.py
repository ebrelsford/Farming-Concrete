from django.db.models import Count

from actstream.models import Action
from django_filters import FilterSet, DateFilter
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import ActionSerializer


class ActionFilter(FilterSet):
    min_timestamp = DateFilter(name='timestamp', lookup_type='gte')
    max_timestamp = DateFilter(name='timestamp', lookup_type='lte')

    class Meta:
        model = Action
        fields = ['timestamp',]


class ActionsViewset(viewsets.ReadOnlyModelViewSet):
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
