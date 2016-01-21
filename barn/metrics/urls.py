from django.conf.urls import url

from .views import DeleteRecordView


urlpatterns = [

    url(r'^delete/(?P<record_type_pk>\d+)/(?P<pk>\d+)/$',
        DeleteRecordView.as_view(),
        name='metrics_delete_record'
    ),

]
