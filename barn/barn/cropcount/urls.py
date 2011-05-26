from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cropcount.views.index'),
    (r'^add/$', 'cropcount.views.add_garden'),
    (r'^beds/(?P<id>\d+)/$', 'cropcount.views.bed_details'),
    (r'^beds/(?P<id>\d+)/delete/$', 'cropcount.views.delete_bed'),
    (r'^patches/(?P<id>\d+)/delete/$', 'cropcount.views.delete_patch'),
)
