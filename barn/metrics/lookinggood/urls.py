from django.conf.urls import url

from .views import (LookingGoodEventAllGardensView,
                    LookingGoodEventGardenDetails, LookingGoodEventIndex)


urlpatterns = [

    url(r'^event/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventIndex.as_view(),
        name='lookinggood_event_index'
    ),


    # Garden lists

    url(r'^event/recorded/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventAllGardensView.as_view(),
        name='lookinggood_event_all_gardens'
    ),


    # Garden details

    url(r'^event/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        LookingGoodEventGardenDetails.as_view(),
        name='lookinggood_event_garden_details',
    ),

]
