from django.conf.urls import patterns, url

from .views import CreateVarietyView, VarietyPickerListView


urlpatterns = patterns('',
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),

    url(r'^varieties/add/',
        CreateVarietyView.as_view(),
        name='farmingconcrete_varieties_add',
    ),

    url(r'^varieties/',
        VarietyPickerListView.as_view(),
        name='farmingconcrete_varieties',
    ),
)
