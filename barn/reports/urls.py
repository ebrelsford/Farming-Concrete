from django.conf.urls import patterns, url

from .views import Index, ExportView, ReportView


main_patterns = patterns('reports.views',
    url(r'^(?P<year>\d+)?', Index.as_view(), name='reports_index'),
)

garden_patterns = patterns('reports.views',
    url(r'^export/', ExportView.as_view(), name='reports_export'),
    url(r'^(?P<year>\d{4})/pdf/', ReportView.as_view(), name='reports_pdf'),
)
