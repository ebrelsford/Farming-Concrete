from django.conf.urls import url

from .views import DonationGardenDetails


urlpatterns = [

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        DonationGardenDetails.as_view(),
        name='donations_garden_details',
    ),

]
