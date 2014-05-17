from django.conf.urls import patterns, url

from .views import SaleGardenCSV, SaleGardenDetails


urlpatterns = patterns('',

    # Garden details

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        SaleGardenDetails.as_view(),
        name='sales_garden_details',
    ),

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        SaleGardenCSV.as_view(),
        name='sales_garden_csv',
    ),

)
