from django.conf.urls import patterns, url

from .views import Index


main_patterns = patterns('reports.views',
    url(r'^shared/(?P<access_key>.+)/$', 'shared_garden_report'),
    url(r'^(?P<year>\d+)?', Index.as_view(), name='reports_index'),
)

garden_patterns = patterns('reports.views',
    (r'^$', 'garden_report'),
    (r'^(?P<year>\d{4})/$', 'garden_report'),
    (r'^(?P<year>\d{4})/share/$', 'share'),
    (r'^(?P<year>\d{4})/pdf/$', 'pdf'),
    (r'^(?P<year>\d{4})/charts/plants_per_crop/$', 'bar_chart_plants_per_crop'),
    (r'^(?P<year>\d{4})/charts/weight_per_crop/$', 'bar_chart_weight_per_crop'),
    (r'^(?P<year>\d{4})/charts/weight_per_gardener/$', 'bar_chart_weight_per_gardener'),
)
