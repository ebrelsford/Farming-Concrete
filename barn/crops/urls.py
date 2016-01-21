from django.conf.urls import url

from .views import CreateCropView, CreateVarietyView, ListVarietiesView


urlpatterns = [

    url(r'^crop/add/', CreateCropView.as_view(), name='crops_crop_add'),

    url(r'^variety/add/', CreateVarietyView.as_view(),
        name='crops_variety_add'),

    url(r'^variety/list/', ListVarietiesView.as_view(),
        name='crops_variety_list'),

]
