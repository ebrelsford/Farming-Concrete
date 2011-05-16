from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'harvestcount.views.index'),
    (r'^harvests/add/$', 'harvestcount.views.add_garden'),
    (r'^gardens/(?P<id>\d+)/$', 'harvestcount.views.garden_details'),
    (r'^gardens/harvested/geojson/$', 'harvestcount.geo.harvested_geojson'),
)
