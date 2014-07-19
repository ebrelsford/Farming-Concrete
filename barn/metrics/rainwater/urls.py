from django.conf.urls import patterns, url

from .views import RainwaterHarvestIndex, RainwaterHarvestGardenDetails


urlpatterns = patterns('',

    #
    # RainwaterHarvest
    #

    url(r'^harvest/(?:(?P<year>\d{4})/)?$',
        RainwaterHarvestIndex.as_view(),
        name='rainwater_harvest_index'
    ),


    # Garden details

    url(r'^harvest/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        RainwaterHarvestGardenDetails.as_view(),
        name='rainwater_harvest_garden_details',
    ),

)
