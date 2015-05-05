from django.conf.urls import patterns, url

from .views import (AcceptGardenGroupMembership, ApproveGardenGroupMembership,
                    AddSuggestedGardenView, CheckGardenGroupMembershipAccess,
                    CreateGardenView, CreateGardenGroupView, GardenDetails,
                    GardenGroupDetailView, GardenSuggestionView,
                    InviteGardenView, RequestGardenGroupMembership,
                    UserGardens, UserGardenLeaveView, UpdateGardenView,
                    UpdateGardenGroupView, UserGardenLeaveConfirmedView)


urlpatterns = patterns('',

    #
    # View
    #

    url(r'^geojson', 'farmingconcrete.views.gardens_geojson',
        name='farmingconcrete_gardens_geojson'
    ),

    url(r'^$', UserGardens.as_view(), name='farmingconcrete_gardens_user'),

    # XXX not ideal, but django.js wasn't taking optional bits of URLs
    url(r'^(?P<year>\d{4})/$', UserGardens.as_view(),
        name='farmingconcrete_gardens_user_by_year'),

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

    url(r'^group/membership/(?P<pk>\d+)/accept/$', 
        AcceptGardenGroupMembership.as_view(),
        name='farmingconcrete_gardengroup_accept'),

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

    url(r'^group/(?P<pk>\d+)/approve/(?P<garden_pk>\d+)/', 
        ApproveGardenGroupMembership.as_view(),
        name='farmingconcrete_gardengroup_approve',
    ),

    url(r'^group/(?P<pk>\d+)/invite/', 
        InviteGardenView.as_view(),
        name='farmingconcrete_gardengroup_invite',
    ),

)
