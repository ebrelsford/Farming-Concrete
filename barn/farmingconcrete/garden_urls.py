from django.conf.urls import patterns, url

from .views import (AcceptGardenGroupMembership, AddSuggestedGardenView,
                    CheckGardenGroupMembershipAccess, CreateGardenView,
                    CreateGardenGroupView, GardenDetails,
                    GardenGroupDetailView, GardenSuggestionView,
                    RequestGardenGroupMembership, UserGardens,
                    UserGardenLeaveView, UpdateGardenView,
                    UpdateGardenGroupView, UserGardenLeaveConfirmedView)


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

    #
    # Groups
    #

    url(r'^group/add/$', CreateGardenGroupView.as_view(),
        name='farmingconcrete_gardengroup_add'),

    url(r'^group/(?P<pk>\d+)/$', GardenGroupDetailView.as_view(),
        name='farmingconcrete_gardengroup_detail',
    ),

    url(r'^group/(?P<pk>\d+)/edit/$', UpdateGardenGroupView.as_view(),
        name='farmingconcrete_gardengroup_update',
    ),

    url(r'^group/(?P<pk>\d+)/can-join/', 
        CheckGardenGroupMembershipAccess.as_view(),
        name='farmingconcrete_gardengroup_can_join',
    ),

    url(r'^group/(?P<pk>\d+)/request/', 
        RequestGardenGroupMembership.as_view(),
        name='farmingconcrete_gardengroup_request',
    ),

    url(r'^group/(?P<pk>\d+)/accept/(?P<garden_pk>\d+)/', 
        AcceptGardenGroupMembership.as_view(),
        name='farmingconcrete_gardengroup_accept',
    ),

)
