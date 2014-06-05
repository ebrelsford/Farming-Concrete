from django.conf.urls import patterns


urlpatterns = patterns('',

    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),

)
