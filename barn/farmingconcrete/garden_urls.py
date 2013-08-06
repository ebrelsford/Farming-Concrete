from django.conf.urls.defaults import patterns, url

from .views import (AddSuggestedGardenView, CreateGardenView,
                    FarmingConcreteGardenDetails, GardenListView,
                    GardenSuggestionView, UserGardensListView,
                    UserGardenLeaveView, UserGardenLeaveConfirmedView)


urlpatterns = patterns('',

    url(r'^$',
        GardenListView.as_view(),
        name='farmingconcrete_gardens',
    ),

    (r'^geojson', 'farmingconcrete.views.gardens_geojson'),

    url(r'^(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        FarmingConcreteGardenDetails.as_view(),
        name='farmingconcrete_garden_details'
    ),

    url(r'^add/$',
        CreateGardenView.as_view(),
        name='farmingconcrete_gardens_add',
    ),

    url(r'^suggest/add/(?P<pk>\d+)/$',
        AddSuggestedGardenView.as_view(),
        name='farmingconcrete_gardens_suggest_add',
    ),

    url(r'^suggest/',
        GardenSuggestionView.as_view(),
        name='farmingconcrete_gardens_suggest',
    ),

    url(r'^yours/$',
        UserGardensListView.as_view(),
        name='farmingconcrete_gardens_yours',
    ),

    url(r'^yours/(?P<pk>\d+)/leave/$',
        UserGardenLeaveView.as_view(),
        name='farmingconcrete_gardens_yours_leave',
    ),

    url(r'^yours/(?P<pk>\d+)/leave/confirmed/$',
        UserGardenLeaveConfirmedView.as_view(),
        name='farmingconcrete_gardens_yours_leave_confirmed',
    ),

)
