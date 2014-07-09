from django.conf.urls import patterns, url

from .views import AddAdminView, DeleteAdminView, DeleteMemberView


urlpatterns = patterns('',

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
