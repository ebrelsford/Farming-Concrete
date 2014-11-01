from django.conf.urls import patterns, url

from .views import Index, SpreadsheetView, PDFView


main_patterns = patterns('',
    url(r'^(?P<year>\d+)?', Index.as_view(), name='reports_index'),
)

garden_patterns = patterns('',
    url(r'^export/', SpreadsheetView.as_view(), name='reports_export'),
    url(r'^pdf/', PDFView.as_view(), name='reports_pdf'),
)
