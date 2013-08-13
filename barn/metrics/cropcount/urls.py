from django.conf.urls.defaults import patterns, url

from .views import CropcountIndex, ConfirmDeletePatchView


urlpatterns = patterns('metrics.cropcount.views',

    url(r'^(?:(?P<year>\d{4})/)?$',
        CropcountIndex.as_view(),
        name='cropcount_index'
    ),


    # Garden lists

    url(r'^yours/(?:(?P<year>\d{4})/)?$',
        'user_gardens',
        name='cropcount_user_gardens'
    ),

    url(r'^counted/(?:(?P<year>\d{4})/)?$',
        'all_gardens',
        name='cropcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?$',
        'garden_details',
        name='cropcount_garden_details'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?summary/$',
        'summary',
        name='cropcount_summary'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        'download_garden_cropcount_as_csv',
        name='cropcount_download_garden_cropcount_as_csv'
    ),


    # Add

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?beds/add/$',
        'add_bed',
        name='cropcount_add_bed'
    ),


    # Beds

    url(r'^beds/(?P<id>\d+)/$',
        'bed_details',
        name='cropcount_bed_details'
    ),

    url(r'^beds/(?P<id>\d+)/delete/$',
        'delete_bed',
        name='cropcount_delete_bed'
    ),


    # Patches

    url(r'^beds/(?P<bed_id>\d+)/patches/add/',
        'add_patch',
        name='cropcount_add_patch'
    ),

    url(r'^patches/(?P<id>\d+)/confirm-delete/$',
        ConfirmDeletePatchView.as_view(),
        name='cropcount_patches_confirm_delete',
    ),

    url(r'^patches/(?P<id>\d+)/delete/$',
        'delete_patch',
        name='cropcount_delete_patch'
    ),
)
