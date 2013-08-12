from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$',
        'metrics.harvestcount.views.index',
        name='harvestcount_index'
    ),
    url(r'^harvests/(?P<id>\d+)/delete/$',
        'metrics.harvestcount.views.delete_harvest',
        name='harvestcount_delete_harvest'
    ),
)
