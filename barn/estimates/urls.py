from django.conf.urls import patterns, url

from .views import ExplainEstimatedYieldView

urlpatterns = patterns('',
    url(r'^estimatedyield/explain/',
        ExplainEstimatedYieldView.as_view(),
        name='estimates_estimatedyield_explain',
    ),
)
