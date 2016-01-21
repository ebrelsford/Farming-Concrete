from django.conf.urls import url

from .views import (SmartsAndSkillsAllGardensView,
                    SmartsAndSkillsGardenDetails, SmartsAndSkillsIndex)


urlpatterns = [

    url(r'^smarts/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsIndex.as_view(),
        name='skills_smarts_index'
    ),


    # Garden lists

    url(r'^smarts/recorded/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsAllGardensView.as_view(),
        name='skills_smarts_all_gardens'
    ),


    # Garden details

    url(r'^smarts/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        SmartsAndSkillsGardenDetails.as_view(),
        name='skills_smarts_garden_details',
    ),

]
