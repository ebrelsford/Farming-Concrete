from django.conf.urls.defaults import patterns, url

from .views import ConfirmDeletePatchView


urlpatterns = patterns('',
    url(r'^$',
        'metrics.cropcount.views.index',
        name='cropcount_index'
    ),

    url(r'^beds/(?P<id>\d+)/$',
        'metrics.cropcount.views.bed_details',
        name='cropcount_bed_details'
    ),

    url(r'^beds/(?P<id>\d+)/delete/$',
        'metrics.cropcount.views.delete_bed',
        name='cropcount_delete_bed'
    ),

    url(r'^beds/(?P<bed_id>\d+)/patches/add/',
        'metrics.cropcount.views.add_patch',
        name='cropcount_add_patch'
    ),

    url(r'^patches/(?P<id>\d+)/confirm-delete/$',
        ConfirmDeletePatchView.as_view(),
        name='cropcount_patches_confirm_delete',
    ),

    url(r'^patches/(?P<id>\d+)/delete/$',
        'metrics.cropcount.views.delete_patch',
        name='cropcount_delete_patch'
    ),
)
