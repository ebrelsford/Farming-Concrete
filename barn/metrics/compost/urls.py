from django.conf.urls import patterns, url

from .views import (WeightAllGardensView, WeightGardenDetails, WeightGardenCSV,
                    WeightIndex, WeightUserGardensView)
from .views import (VolumeAllGardensView, VolumeGardenDetails, VolumeGardenCSV,
                    VolumeIndex, VolumeUserGardensView)


urlpatterns = patterns('',

    #
    # Weight
    #

    url(r'^weight/(?:(?P<year>\d{4})/)?$',
        WeightIndex.as_view(),
        name='compostproduction_weight_index'
    ),


    # Garden lists

    url(r'^weight/recorded/(?:(?P<year>\d{4})/)?$',
        WeightAllGardensView.as_view(),
        name='compostproduction_weight_all_gardens'
    ),

    url(r'^weight/yours/(?:(?P<year>\d{4})/)?$',
        WeightUserGardensView.as_view(),
        name='compostproduction_weight_user_gardens'
    ),


    # Garden details

    url(r'^weight/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        WeightGardenDetails.as_view(),
        name='compostproduction_weight_garden_details',
    ),

    url(r'^weight/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        WeightGardenCSV.as_view(),
        name='compostproduction_weight_garden_csv',
    ),


    #
    # Volume
    #

    url(r'^volume/(?:(?P<year>\d{4})/)?$',
        VolumeIndex.as_view(),
        name='compostproduction_volume_index'
    ),


    # Garden lists

    url(r'^volume/recorded/(?:(?P<year>\d{4})/)?$',
        VolumeAllGardensView.as_view(),
        name='compostproduction_volume_all_gardens'
    ),

    url(r'^volume/yours/(?:(?P<year>\d{4})/)?$',
        VolumeUserGardensView.as_view(),
        name='compostproduction_volume_user_gardens'
    ),


    # Garden details

    url(r'^volume/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        VolumeGardenDetails.as_view(),
        name='compostproduction_volume_garden_details',
    ),

    url(r'^volume/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        VolumeGardenCSV.as_view(),
        name='compostproduction_volume_garden_csv',
    ),

)
