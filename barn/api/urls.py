from django.conf.urls import patterns, url

from .views import RecordsView


urlpatterns = patterns('',
    url(r'^records/', RecordsView.as_view(), name='api_records'),
)
