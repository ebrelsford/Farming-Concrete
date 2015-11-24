from django.conf.urls import url, include

from rest_framework import routers

from .views import ActionsViewset, ActionsSummaryView

router = routers.DefaultRouter()
router.register(r'actions', ActionsViewset)

urlpatterns = [
    url(r'^actions/summary/', ActionsSummaryView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
