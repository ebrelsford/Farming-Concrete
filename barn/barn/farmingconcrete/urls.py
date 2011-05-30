from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),
)
