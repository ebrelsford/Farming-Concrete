from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'farmingconcrete.views.index'),

    (r'^cropcount/', include('cropcount.urls')),
    (r'^harvestcount/', include('harvestcount.urls')),
    (r'^fc/', include('farmingconcrete.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),

    (r'^gardens/geojson', 'farmingconcrete.views.gardens_geojson'),

    (r'^gardens/(?P<id>\d+)/cropcount/$', 'cropcount.views.garden_details'),
    (r'^gardens/cropcount/yours/$', 'cropcount.views.user_gardens'),
    (r'^gardens/cropcount/counted/$', 'cropcount.views.all_gardens'),

    (r'^gardens/(?P<id>\d+)/harvestcount/$', 'harvestcount.views.garden_details'),
    (r'^gardens/(?P<id>\d+)/harvestcount/last_harvest', 'harvestcount.views.quantity_for_last_harvest'),
    (r'^gardens/harvestcount/yours/$', 'harvestcount.views.user_gardens'),
    (r'^gardens/harvestcount/harvested/$', 'harvestcount.views.all_gardens'),

    (r'^ajax_select/', include('ajax_select.urls')),

    # auth
    (r'^accounts/$', 'farmingconcrete.views.account'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/password/change/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/confirm?uid=(?P<uidb36>.*)&token=(?P<token>.*)$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^accounts/password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

handler500 = 'barn.views.server_error'
