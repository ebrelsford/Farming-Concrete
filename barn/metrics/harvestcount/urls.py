from django.conf.urls import patterns, url

from .views import (CreateGardenerView, GardenDetails, GardenerAddView,
                    HarvestcountAllGardensView, HarvestcountIndex,
                    HarvestcountUserGardenView)


urlpatterns = patterns('',

    url(r'^(?:(?P<year>\d{4})/)?$',
        HarvestcountIndex.as_view(),
        name='harvestcount_index'
    ),


    # Garden lists

    url(r'^yours/(?:(?P<year>\d{4})/)?$',
        HarvestcountUserGardenView.as_view(),
        name='harvestcount_user_gardens'
    ),

    url(r'^harvested/(?:(?P<year>\d{4})/)?$',
        HarvestcountAllGardensView.as_view(),
        name='harvestcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        GardenDetails.as_view(),
        name='harvestcount_garden_details',
    ),

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?csv/$',
        'metrics.harvestcount.views.download_garden_harvestcount_as_csv',
        name='harvestcount_download_garden_harvestcount_as_csv'
    ),


    # Add / delete harvests

    url(r'^harvests/(?P<id>\d+)/delete/$',
        'metrics.harvestcount.views.delete_harvest',
        name='harvestcount_delete_harvest'
    ),

    url(r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?gardeners/add/$',
        GardenerAddView.as_view(),
        name='harvestcount_add_gardener',
    ),

    url(r'^gardener/add/$',
        CreateGardenerView.as_view(),
        name='harvestcount_gardener_add',
    ),


    # Other

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?last_harvest',
        'metrics.harvestcount.views.quantity_for_last_harvest',
        name='harvestcount_quantity_for_last_harvest'
    ),

)
