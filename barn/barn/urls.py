from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    (r'^cropcount/', include('cropcount.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),

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
