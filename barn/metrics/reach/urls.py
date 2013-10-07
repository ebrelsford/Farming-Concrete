from django.conf.urls.defaults import patterns, url

from .views import (ProgramReachAllGardensView, ProgramReachGardenDetails,
                    ProgramReachGardenCSV, ProgramReachIndex,
                    ProgramReachUserGardensView)


urlpatterns = patterns('',

    url(r'^program/(?:(?P<year>\d{4})/)?$',
        ProgramReachIndex.as_view(),
        name='reach_program_index'
    ),


    # Garden lists

    url(r'^program/recorded/(?:(?P<year>\d{4})/)?$',
        ProgramReachAllGardensView.as_view(),
        name='reach_program_all_gardens'
    ),

    url(r'^program/yours/(?:(?P<year>\d{4})/)?$',
        ProgramReachUserGardensView.as_view(),
        name='reach_program_user_gardens'
    ),


    # Garden details

    url(r'^program/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        ProgramReachGardenDetails.as_view(),
        name='reach_program_garden_details',
    ),

    url(r'^program/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        ProgramReachGardenCSV.as_view(),
        name='reach_program_garden_csv',
    ),

)
