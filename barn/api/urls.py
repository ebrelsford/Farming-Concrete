from django.conf.urls import url

from .views import (AvailableFiltersView, SpreadsheetView, OverviewView,
                    RecordsView)


urlpatterns = [
    url(r'^export/', SpreadsheetView.as_view(), name='api_export'),
    url(r'^filters/available/', AvailableFiltersView.as_view(),
        name='api_available_filters'),
    url(r'^overview/', OverviewView.as_view(), name='api_overview'),
    url(r'^records/', RecordsView.as_view(), name='api_records'),
]
