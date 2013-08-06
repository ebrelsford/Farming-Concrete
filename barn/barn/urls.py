from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from django.conf import settings

import accounts.urls
from farmingconcrete.views import IndexView, FarmingConcreteGardenDetails
from harvestcount.views import GardenerAddView, HarvestAddView
import reports.urls

urlpatterns = patterns('',
    url(r'^(?:(?P<year>\d{4})/)?$',
        IndexView.as_view(),
        name='farmingconcrete_index'
    ),
    url(r'^gardens/(?P<pk>\d+)/(?:(?P<year>\d{4})/)?$',
        FarmingConcreteGardenDetails.as_view(),
        name='farmingconcrete_garden_details'
    ),
    (r'^gardens/geojson', 'farmingconcrete.views.gardens_geojson'),

    # crop count
    (r'^cropcount/(?:(?P<year>\d{4})/)?', include('cropcount.urls')),
    (r'^cropcount/yours/(?:(?P<year>\d{4})/)?$', 'cropcount.views.user_gardens'),
    (r'^cropcount/counted/(?:(?P<year>\d{4})/)?$', 'cropcount.views.all_gardens'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?$', 'cropcount.views.garden_details'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?summary/$', 'cropcount.views.summary'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?csv/$', 'cropcount.views.download_garden_cropcount_as_csv'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?beds/add/$', 'cropcount.views.add_bed'),

    # harvest count
    (r'^harvestcount/(?:(?P<year>\d{4})/)?', include('harvestcount.urls')),
    (r'^harvestcount/yours/(?:(?P<year>\d{4})/)?$', 'harvestcount.views.user_gardens'),
    (r'^harvestcount/harvested/(?:(?P<year>\d{4})/)?$', 'harvestcount.views.all_gardens'),
    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?$',
        'harvestcount.views.garden_details',
        name='harvestcount_garden_details',
    ),

    url(r'^estimates/', include('estimates.urls')),

    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?harvests/add/',
        HarvestAddView.as_view(),
        name='harvestcount_add_harvest',
    ),

    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?gardeners/add/$',
        GardenerAddView.as_view(),
        name='harvestcount_add_gardener',
    ),

    (r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?csv/$', 'harvestcount.views.download_garden_harvestcount_as_csv'),
    (r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?last_harvest', 'harvestcount.views.quantity_for_last_harvest'),

    # reports
    url(r'^reports/', include(reports.urls.main_patterns)),
    url(r'^gardens/(?P<id>\d+)/report/', include(reports.urls.garden_patterns)),

    # auth
    (r'^accounts/$', 'farmingconcrete.views.account'),
    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$',
     'accounts.views.password_reset'),
    (r'^accounts/registration/',
     include('registration.backends.default.urls')),
    (r'^accounts/', include(accounts.urls.built_in_auth_urls)),

    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # miscellany
    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^fc/', include('farmingconcrete.urls')),
    url(r'^djangojs/', include('djangojs.urls')),

    (r'^harvestmap/$', 'harvestmap.views.map'),
    (r'^harvestmap/gardens/kml', 'harvestmap.views.kml'),
    (r'^harvestmap/data', 'harvestmap.views.data'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler500 = 'barn.views.server_error'
