from django.conf.urls.defaults import patterns, url

from .views import (RecipeTallyAllGardensView, RecipeTallyGardenDetails,
                    RecipeTallyGardenCSV, RecipeTallyIndex,
                    RecipeTallyUserGardensView)


urlpatterns = patterns('',

    url(r'^tally/(?:(?P<year>\d{4})/)?$',
        RecipeTallyIndex.as_view(),
        name='recipes_tally_index'
    ),


    # Garden lists

    url(r'^tally/recorded/(?:(?P<year>\d{4})/)?$',
        RecipeTallyAllGardensView.as_view(),
        name='recipes_tally_all_gardens'
    ),

    url(r'^tally/yours/(?:(?P<year>\d{4})/)?$',
        RecipeTallyUserGardensView.as_view(),
        name='recipes_tally_user_gardens'
    ),


    # Garden details

    url(r'^tally/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        RecipeTallyGardenDetails.as_view(),
        name='recipes_tally_garden_details',
    ),

    url(r'^tally/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        RecipeTallyGardenCSV.as_view(),
        name='recipes_tally_garden_csv',
    ),

)
