from django.conf.urls.defaults import patterns, url

from .views import (WeightAllGardensView, WeightGardenDetails, WeightIndex,
                    WeightUserGardensView)


urlpatterns = patterns('',

    url(r'^weight/(?:(?P<year>\d{4})/)?$',
        WeightIndex.as_view(),
        name='landfilldiversion_weight_index'
    ),


    # Garden lists

    url(r'^weight/recorded/(?:(?P<year>\d{4})/)?$',
        WeightAllGardensView.as_view(),
        name='landfilldiversion_weight_all_gardens'
    ),

    url(r'^weight/yours/(?:(?P<year>\d{4})/)?$',
        WeightUserGardensView.as_view(),
        name='landfilldiversion_weight_user_gardens'
    ),


    # Garden details

    url(r'^weight/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        WeightGardenDetails.as_view(),
        name='landfilldiversion_weight_garden_details',
    ),

)
