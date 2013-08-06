from django.conf.urls.defaults import patterns, url

from .views import VarietyPickerListView, VarietyAddView


urlpatterns = patterns('',
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),

    url(r'^varieties/add/',
        VarietyAddView.as_view(),
        name='farmingconcrete_varieties_add',
    ),

    url(r'^varieties/',
        VarietyPickerListView.as_view(),
        name='farmingconcrete_varieties',
    ),
)
