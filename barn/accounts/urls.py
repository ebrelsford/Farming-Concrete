from django.conf.urls import patterns, url

built_in_auth_urls = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^password/change/$', 'password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        name='password_change_done'),
    url(r'^password/reset/$', 'password_reset'),
    url(r'^password/reset/done/$', 'password_reset_done',
        name='password_reset_done'),
    url(r'^password/reset/confirm?uid=(?P<uidb64>.*)&token=(?P<token>.*)$',
        'password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete',
        name='password_reset_complete'),
)
