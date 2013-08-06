from django.conf.urls.defaults import patterns, url

from .views import (AddSuggestedGardenView, CreateGardenView, GardenListView,
                    GardenSuggestionView, UserGardensListView,
                    VarietyPickerListView, VarietyAddView)


urlpatterns = patterns('',
    (r'^type/(?P<type>\w+)$', 'farmingconcrete.views.switch_garden_type'),

    url(r'^gardens/$',
        GardenListView.as_view(),
        name='farmingconcrete_gardens',
    ),

    url(r'^gardens/add/$',
        CreateGardenView.as_view(),
        name='farmingconcrete_gardens_add',
    ),

    url(r'^gardens/suggest/add/(?P<pk>\d+)/$',
        AddSuggestedGardenView.as_view(),
        name='farmingconcrete_gardens_suggest_add',
    ),

    url(r'^gardens/suggest/',
        GardenSuggestionView.as_view(),
        name='farmingconcrete_gardens_suggest',
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
