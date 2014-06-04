from django.conf.urls import patterns, url

from .views import CreateCropView


urlpatterns = patterns('',

    url(r'^crop/add/', CreateCropView.as_view(), name='crops_crop_add'),

)
