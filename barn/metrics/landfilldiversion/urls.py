from django.conf.urls import patterns, url

from .views import (WeightAllGardensView, WeightGardenDetails, WeightGardenCSV,
                    WeightIndex)
from .views import (VolumeAllGardensView, VolumeGardenDetails, VolumeGardenCSV,
                    VolumeIndex, VolumeSummaryJSON)


urlpatterns = patterns('',

    #
    # Weight
    #

    url(r'^weight/(?:(?P<year>\d{4})/)?$',
        WeightIndex.as_view(),
        name='landfilldiversion_weight_index'
    ),


    # Garden lists

    url(r'^weight/recorded/(?:(?P<year>\d{4})/)?$',
        WeightAllGardensView.as_view(),
        name='landfilldiversion_weight_all_gardens'
    ),


    # Garden details

    url(r'^weight/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        WeightGardenDetails.as_view(),
        name='landfilldiversion_weight_garden_details',
    ),

    url(r'^weight/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        WeightGardenCSV.as_view(),
        name='landfilldiversion_weight_garden_csv',
    ),


    #
    # Volume
    #

    url(r'^volume/(?:(?P<year>\d{4})/)?$',
        VolumeIndex.as_view(),
        name='landfilldiversion_volume_index'
    ),


    # Garden lists

    url(r'^volume/recorded/(?:(?P<year>\d{4})/)?$',
        VolumeAllGardensView.as_view(),
        name='landfilldiversion_volume_all_gardens'
    ),


    # Garden details

    url(r'^volume/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        VolumeGardenDetails.as_view(),
        name='landfilldiversion_volume_garden_details',
    ),

    url(r'^volume/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        VolumeGardenCSV.as_view(),
        name='landfilldiversion_volume_garden_csv',
    ),

    url(r'^volume/data/json/',
        VolumeSummaryJSON.as_view(),
        name='landfilldiversion_volume_data',
    ),

)
