from django.conf.urls import patterns, url

from .views import (CreateGardenerView, GardenDetails, GardenerAddView,
                    HarvestcountAllGardensView, HarvestcountIndex)


urlpatterns = patterns('',

    url(r'^(?:(?P<year>\d{4})/)?$',
        HarvestcountIndex.as_view(),
        name='harvestcount_index'
    ),


    # Garden lists

    url(r'^harvested/(?:(?P<year>\d{4})/)?$',
        HarvestcountAllGardensView.as_view(),
        name='harvestcount_all_gardens'
    ),


    # Garden details

    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        GardenDetails.as_view(),
        name='harvestcount_garden_details',
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
