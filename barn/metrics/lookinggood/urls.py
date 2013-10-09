from django.conf.urls.defaults import patterns, url

from .views import (LookingGoodEventAllGardensView,
                    LookingGoodEventGardenDetails, LookingGoodEventGardenCSV,
                    LookingGoodEventIndex, LookingGoodEventUserGardensView)


urlpatterns = patterns('',

    url(r'^event/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventIndex.as_view(),
        name='lookinggood_event_index'
    ),


    # Garden lists

    url(r'^event/recorded/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventAllGardensView.as_view(),
        name='lookinggood_event_all_gardens'
    ),

    url(r'^event/yours/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventUserGardensView.as_view(),
        name='lookinggood_event_user_gardens'
    ),


    # Garden details

    url(r'^event/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventGardenDetails.as_view(),
        name='lookinggood_event_garden_details',
    ),

    url(r'^event/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        LookingGoodEventGardenCSV.as_view(),
        name='lookinggood_event_garden_csv',
    ),

)
