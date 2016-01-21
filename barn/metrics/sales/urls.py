from django.conf.urls import url

from .views import SaleGardenDetails


urlpatterns = [

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        SaleGardenDetails.as_view(),
        name='sales_garden_details',
    ),

]
