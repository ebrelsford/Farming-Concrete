from django.conf.urls import patterns, url

from .views import (RainwaterHarvestGardenCSV, RainwaterHarvestIndex,
                    RainwaterHarvestGardenDetails)


urlpatterns = patterns('',

    #
    # RainwaterHarvest
    #

    url(r'^harvest/(?:(?P<year>\d{4})/)?$',
        RainwaterHarvestIndex.as_view(),
        name='rainwater_harvest_index'
    ),


    # Garden lists

    # url(r'^harvest/recorded/(?:(?P<year>\d{4})/)?$',
    #     RainwaterHarvestAllGardensView.as_view(),
    #     name='rainwater_harvest_all_gardens'
    # ),

    # url(r'^harvest/yours/(?:(?P<year>\d{4})/)?$',
    #     RainwaterHarvestUserGardensView.as_view(),
    #     name='rainwater_harvest_user_gardens'
    # ),


    # Garden details

    url(r'^harvest/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        RainwaterHarvestGardenDetails.as_view(),
        name='rainwater_harvest_garden_details',
    ),

    url(r'^harvest/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        RainwaterHarvestGardenCSV.as_view(),
        name='rainwater_harvest_garden_csv',
    ),

)
