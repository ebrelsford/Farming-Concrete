from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'harvestcount.views.index'),
    (r'^harvests/add/$', 'harvestcount.views.add_garden'),
    (r'^gardens/harvested/geojson/$', 'harvestcount.geo.harvested_geojson'),
)
