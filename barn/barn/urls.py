from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    (r'^(?:(?P<year>\d{4})/)?$', 'farmingconcrete.views.index'),
    (r'^gardens/(?P<id>\d+)/(?:(?P<year>\d{4})/)?$', 'farmingconcrete.views.garden_details'),
    (r'^gardens/geojson', 'farmingconcrete.views.gardens_geojson'),

    # crop count
    (r'^cropcount/(?:(?P<year>\d{4})/)?', include('cropcount.urls')),
    (r'^cropcount/yours/(?:(?P<year>\d{4})/)?$', 'cropcount.views.user_gardens'),
    (r'^cropcount/counted/(?:(?P<year>\d{4})/)?$', 'cropcount.views.all_gardens'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?$', 'cropcount.views.garden_details'),
    (r'^gardens/(?P<id>\d+)/cropcount/(?:(?P<year>\d{4})/)?csv/$', 'cropcount.views.download_garden_cropcount_as_csv'),

    # harvest count
    (r'^harvestcount/(?:(?P<year>\d{4})/)?', include('harvestcount.urls')),
    (r'^harvestcount/yours/(?:(?P<year>\d{4})/)?$', 'harvestcount.views.user_gardens'),
    (r'^harvestcount/harvested/(?:(?P<year>\d{4})/)?$', 'harvestcount.views.all_gardens'),
    (r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?$', 'harvestcount.views.garden_details'),
    (r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?csv/$', 'harvestcount.views.download_garden_harvestcount_as_csv'),
    (r'^gardens/(?P<id>\d+)/harvestcount/(?:(?P<year>\d{4})/)?last_harvest', 'harvestcount.views.quantity_for_last_harvest'),

    # reports
    (r'^reports/$', 'reports.views.index'),
    (r'^reports/(?P<year>\d+)', 'reports.views.index'), # TODO finish this
                       
    #(r'^reports/borough/(?P<borough>\w+)/$', 'reports.views.borough_report'),
    #(r'^reports/borough/(?P<borough>\w+)/(?P<type>.+)/$', 'reports.views.borough_report'),

    (r'^gardens/(?P<id>\d+)/report/$', 'reports.views.garden_report'),
    (r'^gardens/(?P<id>\d+)/report/charts/plants_per_crop$', 'reports.views.bar_chart_plants_per_crop'),
    (r'^gardens/(?P<id>\d+)/report/charts/weight_per_crop$', 'reports.views.bar_chart_weight_per_crop'),
    (r'^gardens/(?P<id>\d+)/report/charts/weight_per_gardener$', 'reports.views.bar_chart_weight_per_gardener'),
    (r'^gardens/(?P<id>\d+)/report/share$', 'reports.views.share'),
    (r'^gardens/(?P<id>\d+)/report/pdf$', 'reports.views.pdf'),
    (r'^gardens/(?P<id>\d+)/report/pdftest$', 'reports.views.pdftest'),
    (r'^reports/shared/(?P<access_key>.+)/$', 'reports.views.shared_garden_report'),

    # auth
    (r'^accounts/$', 'farmingconcrete.views.account'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password/change/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/confirm?uid=(?P<uidb36>.*)&token=(?P<token>.*)$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # miscellany
    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^fc/', include('farmingconcrete.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
)

handler500 = 'barn.views.server_error'
