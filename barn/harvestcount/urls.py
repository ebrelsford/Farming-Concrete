from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'harvestcount.views.index'),
    (r'^harvests/gardens/add/$', 'harvestcount.views.add_garden'),
    (r'^harvests/(?P<id>\d+)/delete/$', 'harvestcount.views.delete_harvest'),
)
