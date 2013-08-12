from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

import accounts.urls
from farmingconcrete.views import IndexView
from metrics.harvestcount.views import GardenerAddView, HarvestAddView
import reports.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?:(?P<year>\d{4})/)?$',
        IndexView.as_view(),
        name='home'
    ),

    (r'^gardens/', include('farmingconcrete.garden_urls')),

    # crop count
    (r'^metrics/cropcount/', include('metrics.cropcount.urls')),

    # harvest count
    (r'^harvestcount/(?:(?P<year>\d{4})/)?', include('metrics.harvestcount.urls')),
    url(r'^harvestcount/yours/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.user_gardens',
        name='harvestcount_user_gardens'
    ),
    url(r'^harvestcount/harvested/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.all_gardens',
        name='harvestcount_all_gardens'
    ),
    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?$',
        'metrics.harvestcount.views.garden_details',
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

    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?csv/$',
        'metrics.harvestcount.views.download_garden_harvestcount_as_csv',
        name='harvestcount_download_garden_harvestcount_as_csv'
    ),
    url(r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?last_harvest',
        'metrics.harvestcount.views.quantity_for_last_harvest',
        name='harvestcount_quantity_for_last_harvest'
    ),

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
    url(r'feedback/success/', TemplateView.as_view(
        template_name='feedback/feedback_success.html'
    ), name='feedback_success'),
    url(r'feedback/', include('feedback.urls')),

    (r'^harvestmap/$', 'harvestmap.views.map'),
    (r'^harvestmap/gardens/kml', 'harvestmap.views.kml'),
    (r'^harvestmap/data', 'harvestmap.views.data'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler500 = 'barn.views.server_error'
