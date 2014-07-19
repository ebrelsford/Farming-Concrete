from django.conf.urls import patterns, url

from .views import (MoodChangeAllGardensView, MoodChangeGardenDetails,
                    MoodChangeIndex)


urlpatterns = patterns('',

    url(r'^change/(?:(?P<year>\d{4})/)?$',
        MoodChangeIndex.as_view(),
        name='moods_change_index'
    ),


    # Garden lists

    url(r'^change/recorded/(?:(?P<year>\d{4})/)?$',
        MoodChangeAllGardensView.as_view(),
        name='moods_change_all_gardens'
    ),


    # Garden details

    url(r'^change/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        MoodChangeGardenDetails.as_view(),
        name='moods_change_garden_details',
    ),

)
