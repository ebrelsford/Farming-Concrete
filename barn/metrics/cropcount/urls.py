from django.conf.urls.defaults import patterns, url

from .views import ConfirmDeletePatchView


urlpatterns = patterns('',
    url(r'^$',
        'metrics.cropcount.views.index',
        name='cropcount_index'
    ),


    # Garden lists

    url(r'^yours/(?:(?P<year>\d{4})/)?$',
        'metrics.cropcount.views.user_gardens',
        name='cropcount_user_gardens'
    ),

    url(r'^counted/(?:(?P<year>\d{4})/)?$',
        'metrics.cropcount.views.all_gardens',
        name='cropcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?$',
        'metrics.cropcount.views.garden_details',
        name='cropcount_garden_details'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?summary/$',
        'metrics.cropcount.views.summary',
        name='cropcount_summary'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        'metrics.cropcount.views.download_garden_cropcount_as_csv',
        name='cropcount_download_garden_cropcount_as_csv'
    ),


    # Add

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?beds/add/$',
        'metrics.cropcount.views.add_bed',
        name='cropcount_add_bed'
    ),


    # Beds

    url(r'^beds/(?P<id>\d+)/(?:(?P<year>\d{4})/)?$',
        'metrics.cropcount.views.bed_details',
        name='cropcount_bed_details'
    ),

    url(r'^beds/(?P<id>\d+)/(?:(?P<year>\d{4})/)?delete/$',
        'metrics.cropcount.views.delete_bed',
        name='cropcount_delete_bed'
    ),

    url(r'^beds/(?P<bed_id>\d+)/(?:(?P<year>\d{4})/)?patches/add/',
        'metrics.cropcount.views.add_patch',
        name='cropcount_add_patch'
    ),


    # Patches

    url(r'^patches/(?P<id>\d+)/(?:(?P<year>\d{4})/)?confirm-delete/$',
        ConfirmDeletePatchView.as_view(),
        name='cropcount_patches_confirm_delete',
    ),

    url(r'^patches/(?P<id>\d+)/(?:(?P<year>\d{4})/)?delete/$',
        'metrics.cropcount.views.delete_patch',
        name='cropcount_delete_patch'
    ),
)
