from django.conf.urls.defaults import patterns, url

from .views import GardenerAddView, HarvestAddView, HarvestcountIndex


urlpatterns = patterns('',

    url(r'^(?:(?P<year>\d{4})/)?$',
        HarvestcountIndex.as_view(),
        name='harvestcount_index'
    ),


    # Garden lists

    url(r'^yours/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.user_gardens',
        name='harvestcount_user_gardens'
    ),

    url(r'^harvested/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.all_gardens',
        name='harvestcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.garden_details',
        name='harvestcount_garden_details',
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        'metrics.harvestcount.views.download_garden_harvestcount_as_csv',
        name='harvestcount_download_garden_harvestcount_as_csv'
    ),


    # Add / delete harvests

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?harvests/add/',
        HarvestAddView.as_view(),
        name='harvestcount_add_harvest',
    ),

    url(r'^harvests/(?P<id>\d+)/delete/$',
        'metrics.harvestcount.views.delete_harvest',
        name='harvestcount_delete_harvest'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?gardeners/add/$',
        GardenerAddView.as_view(),
        name='harvestcount_add_gardener',
    ),


    # Other

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?last_harvest',
        'metrics.harvestcount.views.quantity_for_last_harvest',
        name='harvestcount_quantity_for_last_harvest'
    ),

)