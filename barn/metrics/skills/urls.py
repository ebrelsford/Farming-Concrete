from django.conf.urls.defaults import patterns, url

from .views import (SmartsAndSkillsAllGardensView,
                    SmartsAndSkillsGardenDetails, SmartsAndSkillsGardenCSV,
                    SmartsAndSkillsIndex, SmartsAndSkillsUserGardensView)


urlpatterns = patterns('',

    url(r'^smarts/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsIndex.as_view(),
        name='skills_smarts_index'
    ),


    # Garden lists

    url(r'^smarts/recorded/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsAllGardensView.as_view(),
        name='skills_smarts_all_gardens'
    ),

    url(r'^smarts/yours/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsUserGardensView.as_view(),
        name='skills_smarts_user_gardens'
    ),


    # Garden details

    url(r'^smarts/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsGardenDetails.as_view(),
        name='skills_smarts_garden_details',
    ),

    url(r'^smarts/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        SmartsAndSkillsGardenCSV.as_view(),
        name='skills_smarts_garden_csv',
    ),

)
