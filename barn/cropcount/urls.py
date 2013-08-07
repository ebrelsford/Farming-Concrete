from django.conf.urls.defaults import *

from cropcount.views import ConfirmDeletePatchView


urlpatterns = patterns('',
    (r'^$', 'cropcount.views.index'),
    (r'^beds/(?P<id>\d+)/$', 'cropcount.views.bed_details'),
    (r'^beds/(?P<id>\d+)/delete/$', 'cropcount.views.delete_bed'),
    (r'^beds/(?P<bed_id>\d+)/patches/add/', 'cropcount.views.add_patch'),

    url(r'^patches/(?P<id>\d+)/confirm-delete/$',
        ConfirmDeletePatchView.as_view(),
        name='cropcount_patches_confirm_delete',
    ),
    (r'^patches/(?P<id>\d+)/delete/$', 'cropcount.views.delete_patch'),
)
