from django.conf.urls import url

from .views import ExplainEstimatedYieldView


urlpatterns = [
    url(r'^estimatedyield/explain/',
        ExplainEstimatedYieldView.as_view(),
        name='estimates_estimatedyield_explain',
    ),
]
