from actstream.models import Action
from rest_framework import permissions, viewsets

from .serializers import ActionSerializer


class ActionsViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
