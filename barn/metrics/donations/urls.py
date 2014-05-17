from django.conf.urls import patterns, url

from .views import DonationGardenCSV, DonationGardenDetails


urlpatterns = patterns('',

    # Garden details

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        DonationGardenDetails.as_view(),
        name='donations_garden_details',
    ),

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        DonationGardenCSV.as_view(),
        name='donations_garden_csv',
    ),

)

