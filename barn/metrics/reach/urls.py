from django.conf.urls import url

from .views import (ProgramReachAllGardensView, ProgramReachGardenDetails,
                    ProgramReachIndex)


urlpatterns = [

    url(r'^program/(?:(?P<year>\d{4})/)?$',
        ProgramReachIndex.as_view(),
        name='reach_program_index'
    ),


    # Garden lists

    url(r'^program/recorded/(?:(?P<year>\d{4})/)?$',
        ProgramReachAllGardensView.as_view(),
        name='reach_program_all_gardens'
    ),


    # Garden details

    url(r'^program/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        ProgramReachGardenDetails.as_view(),
        name='reach_program_garden_details',
    ),

]
