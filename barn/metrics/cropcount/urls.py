from django.conf.urls import patterns, url

from .views import (CropcountIndex, CropcountAllGardensView, CropcountCSV,
                    GardenDetails)


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

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?summary/$',
        'summary',
        name='cropcount_summary'
    ),

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        CropcountCSV.as_view(),
        name='cropcount_download_garden_cropcount_as_csv'
    ),


    # Beds

    url(r'^beds/(?P<id>\d+)/delete/$',
        'delete_bed',
        name='cropcount_delete_bed'
    ),

)
