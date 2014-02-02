from django.conf.urls import patterns, url

from .views import (HoursByGeographyAllGardensView,
                    HoursByGeographyGardenDetails, HoursByGeographyGardenCSV,
                    HoursByGeographyIndex, HoursByGeographyUserGardensView)
from .views import (HoursByTaskAllGardensView, HoursByTaskGardenDetails,
                    HoursByTaskGardenCSV, HoursByTaskIndex,
                    HoursByTaskUserGardensView)
from .views import (HoursByProjectAllGardensView, HoursByProjectGardenDetails,
                    HoursByProjectGardenCSV, HoursByProjectIndex,
                    HoursByProjectUserGardensView)
from .views import CreateProjectView


urlpatterns = patterns('',

    #
    # Hours by geography
    #

    url(r'^geography/(?:(?P<year>\d{4})/)?$',
        HoursByGeographyIndex.as_view(),
        name='participation_geography_index'
    ),


    # Garden lists

    url(r'^geography/recorded/(?:(?P<year>\d{4})/)?$',
        HoursByGeographyAllGardensView.as_view(),
        name='participation_geography_all_gardens'
    ),

    url(r'^geography/yours/(?:(?P<year>\d{4})/)?$',
        HoursByGeographyUserGardensView.as_view(),
        name='participation_geography_user_gardens'
    ),


    # Garden details

    url(r'^geography/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        HoursByGeographyGardenDetails.as_view(),
        name='participation_geography_garden_details',
    ),

    url(r'^geography/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        HoursByGeographyGardenCSV.as_view(),
        name='participation_geography_garden_csv',
    ),


    #
    # Hours by task
    #

    url(r'^task/(?:(?P<year>\d{4})/)?$',
        HoursByTaskIndex.as_view(),
        name='participation_task_index'
    ),


    # Garden lists

    url(r'^task/recorded/(?:(?P<year>\d{4})/)?$',
        HoursByTaskAllGardensView.as_view(),
        name='participation_task_all_gardens'
    ),

    url(r'^task/yours/(?:(?P<year>\d{4})/)?$',
        HoursByTaskUserGardensView.as_view(),
        name='participation_task_user_gardens'
    ),


    # Garden details

    url(r'^task/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        HoursByTaskGardenDetails.as_view(),
        name='participation_task_garden_details',
    ),

    url(r'^task/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        HoursByTaskGardenCSV.as_view(),
        name='participation_task_garden_csv',
    ),


    #
    # Hours by project
    #

    url(r'^project/(?:(?P<year>\d{4})/)?$',
        HoursByProjectIndex.as_view(),
        name='participation_project_index'
    ),


    # Garden lists

    url(r'^project/recorded/(?:(?P<year>\d{4})/)?$',
        HoursByProjectAllGardensView.as_view(),
        name='participation_project_all_gardens'
    ),

    url(r'^project/yours/(?:(?P<year>\d{4})/)?$',
        HoursByProjectUserGardensView.as_view(),
        name='participation_project_user_gardens'
    ),


    # Garden details

    url(r'^project/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        HoursByProjectGardenDetails.as_view(),
        name='participation_project_garden_details',
    ),

    url(r'^project/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        HoursByProjectGardenCSV.as_view(),
        name='participation_project_garden_csv',
    ),


    #
    # Non-record views
    #

    # Projects
    url(r'^project/add/$',
        CreateProjectView.as_view(),
        name='participation_project_add',
    )

)
