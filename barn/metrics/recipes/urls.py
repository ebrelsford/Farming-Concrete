from django.conf.urls import url

from .views import (RecipeTallyAllGardensView, RecipeTallyGardenDetails,
                    RecipeTallyIndex)


urlpatterns = [

    url(r'^tally/(?:(?P<year>\d{4})/)?$',
        RecipeTallyIndex.as_view(),
        name='recipes_tally_index'
    ),


    # Garden lists

    url(r'^tally/recorded/(?:(?P<year>\d{4})/)?$',
        RecipeTallyAllGardensView.as_view(),
        name='recipes_tally_all_gardens'
    ),


    # Garden details

    url(r'^tally/gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        RecipeTallyGardenDetails.as_view(),
        name='recipes_tally_garden_details',
    ),

]
