from django.conf.urls.defaults import patterns, url

from .views import (AddSuggestedGardenView, CreateGardenView,
                    FarmingConcreteGardenDetails, GardenGroupDetailView,
                    GardenSuggestionView, UserGardenLeaveView,
                    UpdateGardenView, UserGardenLeaveConfirmedView)


urlpatterns = patterns('',

    url(r'^geojson', 'farmingconcrete.views.gardens_geojson',
        name='farmingconcrete_gardens_geojson'
    ),

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

    url(r'^(?P<pk>\d+)/edit/$',
        UpdateGardenView.as_view(),
        name='farmingconcrete_gardens_update',
    ),

    url(r'^(?P<pk>\d+)/leave/$',
        UserGardenLeaveView.as_view(),
        name='farmingconcrete_gardens_leave',
    ),

    url(r'^(?P<pk>\d+)/leave/confirmed/$',
        UserGardenLeaveConfirmedView.as_view(),
        name='farmingconcrete_gardens_leave_confirmed',
    ),

    url(r'^group/(?P<pk>\d+)/$',
        GardenGroupDetailView.as_view(),
        name='farmingconcrete_gardengroup_detail',
    ),

)
