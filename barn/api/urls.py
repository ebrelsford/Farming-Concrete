from django.conf.urls import patterns, url

from .views import SpreadsheetView, RecordsView


urlpatterns = patterns('',
    url(r'^export/', SpreadsheetView.as_view(), name='api_export'),
    url(r'^records/', RecordsView.as_view(), name='api_records'),
)
