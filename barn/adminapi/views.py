from datetime import timedelta

from django.db.models import Count
from django.utils.timezone import now

from actstream.models import Action
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import ActionSerializer


class ActionsViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all().order_by('-timestamp')
    serializer_class = ActionSerializer


class ActionsSummaryView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Only get actions from the past year
        queryset = queryset.filter(timestamp__gte=now() - timedelta(days=365))

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
