from django.conf.urls import patterns, url

from .views import (AddSuggestedGardenView, CreateGardenView,
                    CreateGardenGroupView, GardenDetails,
                    GardenGroupDetailView, GardenSuggestionView, UserGardens,
                    UserGardenLeaveView, UpdateGardenView,
                    UserGardenLeaveConfirmedView)


urlpatterns = patterns('',

    #
    # View
    #

    url(r'^geojson', 'farmingconcrete.views.gardens_geojson',
        name='farmingconcrete_gardens_geojson'
    ),

    url(r'^$', UserGardens.as_view(), name='farmingconcrete_gardens_user'),

    url(r'^(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$', GardenDetails.as_view(),
        name='farmingconcrete_garden_details'
    ),

    url(r'^group/add/$', CreateGardenGroupView.as_view(),
        name='farmingconcrete_gardengroup_add'),

    url(r'^group/(?P<pk>\d+)/$', GardenGroupDetailView.as_view(),
        name='farmingconcrete_gardengroup_detail',
    ),

    #
    # Add / edit
    #

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

)
