from django.conf.urls.defaults import patterns, url

from farmingconcrete.views import GardenListView, UserGardensListView, VarietyPickerListView, VarietyAddView

urlpatterns = patterns('',
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),

    url(r'^gardens/$', 
        GardenListView.as_view(), 
        name='farmingconcrete_gardens',
    ),

    url(r'^gardens/yours/$', 
        UserGardensListView.as_view(), 
        name='farmingconcrete_gardens_yours',
    ),

    url(r'^varieties/add/', 
        VarietyAddView.as_view(), 
        name='farmingconcrete_varieties_add',
    ),

    url(r'^varieties/', 
        VarietyPickerListView.as_view(), 
        name='farmingconcrete_varieties',
    ),
)
