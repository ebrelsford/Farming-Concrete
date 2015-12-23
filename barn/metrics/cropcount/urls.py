from django.conf.urls import patterns, url

from .views import CropcountIndex, CropcountAllGardensView, GardenDetails


urlpatterns = patterns('metrics.cropcount.views',

    url(r'^(?:(?P<year>\d{4})/)?$',
        CropcountIndex.as_view(),
        name='cropcount_index'
    ),


    # Garden lists

    url(r'^counted/(?:(?P<year>\d{4})/)?$',
        CropcountAllGardensView.as_view(),
        name='cropcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        GardenDetails.as_view(),
        name='cropcount_garden_details'
    ),


    # Beds

    url(r'^beds/(?P<id>\d+)/delete/$',
        'delete_bed',
        name='cropcount_delete_bed'
    ),

)
