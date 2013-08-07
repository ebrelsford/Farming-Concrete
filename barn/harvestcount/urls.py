from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    (r'^$', 'harvestcount.views.index'),
    (r'^harvests/(?P<id>\d+)/delete/$', 'harvestcount.views.delete_harvest'),
)
