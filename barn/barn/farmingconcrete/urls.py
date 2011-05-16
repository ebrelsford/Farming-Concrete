from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^garden/(?P<id>\d+)/geojson/$', 'farmingconcrete.views.garden_geojson'),
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),
)
