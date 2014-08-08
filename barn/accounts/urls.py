from django.conf.urls import patterns, url

from .views import (AccountDetailsView, AddAdminView, DeleteAdminView,
                    DeleteMemberView, InviteMemberView)


urlpatterns = patterns('',

    url(r'^$',
        AccountDetailsView.as_view(),
        name='account_details',
    ),

    url(r'^gardenmemberships/invite/$',
        InviteMemberView.as_view(),
        name='gardenmemberships_invite',
    ),

    url(r'^gardenmemberships/(?P<pk>\d+)/admin/add/',
        AddAdminView.as_view(),
        name='gardenmemberships_admin_add',
    ),

    url(r'^gardenmemberships/(?P<pk>\d+)/admin/delete/',
        DeleteAdminView.as_view(),
        name='gardenmemberships_admin_delete',
    ),

    url(r'^gardenmemberships/(?P<pk>\d+)/delete/',
        DeleteMemberView.as_view(),
        name='gardenmemberships_member_delete',
    ),

)
