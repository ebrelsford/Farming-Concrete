from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cropcount.views.index'),
    (r'^gardens/$', 'cropcount.views.gardens'),
    (r'^gardens/complete/geojson/$', 'cropcount.views.complete_geojson'),
    (r'^gardens/(?P<id>\d+)/$', 'cropcount.views.garden_details'),
    (r'^gardens/add/$', 'cropcount.views.add_garden'),
    (r'^beds/(?P<id>\d+)/$', 'cropcount.views.bed_details'),
    (r'^beds/(?P<id>\d+)/delete/$', 'cropcount.views.delete_bed'),
    (r'^patches/(?P<id>\d+)/delete/$', 'cropcount.views.delete_patch'),
)
