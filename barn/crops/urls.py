from django.conf.urls import patterns, url

from .views import CreateCropView, CreateVarietyView, ListVarietiesView


urlpatterns = patterns('',

    url(r'^crop/add/', CreateCropView.as_view(), name='crops_crop_add'),

    url(r'^variety/add/', CreateVarietyView.as_view(),
        name='crops_variety_add'),

    url(r'^variety/list/', ListVarietiesView.as_view(),
        name='crops_variety_list'),

)
