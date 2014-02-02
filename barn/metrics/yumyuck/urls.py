from django.conf.urls import patterns, url

from .views import (YumYuckAllGardensView, YumYuckGardenDetails,
                    YumYuckGardenCSV, YumYuckIndex, YumYuckUserGardensView)


urlpatterns = patterns('',

    url(r'^change/(?:(?P<year>\d{4})/)?$',
        YumYuckIndex.as_view(),
        name='yumyuck_change_index'
    ),


    # Garden lists

    url(r'^change/recorded/(?:(?P<year>\d{4})/)?$',
        YumYuckAllGardensView.as_view(),
        name='yumyuck_change_all_gardens'
    ),

    url(r'^change/yours/(?:(?P<year>\d{4})/)?$',
        YumYuckUserGardensView.as_view(),
        name='yumyuck_change_user_gardens'
    ),


    # Garden details

    url(r'^change/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        YumYuckGardenDetails.as_view(),
        name='yumyuck_change_garden_details',
    ),

    url(r'^change/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        YumYuckGardenCSV.as_view(),
        name='yumyuck_change_garden_csv',
    ),

)
