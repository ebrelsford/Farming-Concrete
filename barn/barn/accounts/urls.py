from django.conf.urls.defaults import patterns, url

built_in_auth_urls = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^password/change/$', 'password_change'),
    url(r'^password/change/done/$', 'password_change_done'),
    url(r'^password/reset/done/$', 'password_reset_done'),
    url(r'^password/reset/confirm?uid=(?P<uidb36>.*)&token=(?P<token>.*)$', 'password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete'),
)
