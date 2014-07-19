from django.conf.urls import patterns, url

from .views import SaleGardenDetails


urlpatterns = patterns('',

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        SaleGardenDetails.as_view(),
        name='sales_garden_details',
    ),

)
