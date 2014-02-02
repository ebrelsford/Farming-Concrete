from django.conf.urls import patterns, url

from .views import DeleteRecordView


urlpatterns = patterns('',

    url(r'^delete/(?P<record_type_pk>\d+)/(?P<pk>\d+)/$',
        DeleteRecordView.as_view(),
        name='metrics_delete_record'
    ),

)
