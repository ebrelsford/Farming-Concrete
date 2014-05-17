from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

import accounts.urls
from farmingconcrete.views import IndexView
import reports.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?:(?P<year>\d{4})/)?$',
        IndexView.as_view(),
        name='home'
    ),

    (r'^gardens/', include('farmingconcrete.garden_urls')),

    # compost
    (r'^metrics/compost/', include('metrics.compost.urls')),

    # crop count
    (r'^metrics/cropcount/', include('metrics.cropcount.urls')),

    # donation
    (r'^metrics/donations/', include('metrics.donations.urls')),

    # harvest count
    (r'^metrics/harvestcount/', include('metrics.harvestcount.urls')),

    # landfill diversion
    (r'^metrics/landfilldiversion/', include('metrics.landfilldiversion.urls')),

    # looking good
    (r'^metrics/lookinggood/', include('metrics.lookinggood.urls')),

    # moods
    (r'^metrics/moods/', include('metrics.moods.urls')),

    # participation
    (r'^metrics/participation/', include('metrics.participation.urls')),

    # rainwater
    (r'^metrics/rainwater/', include('metrics.rainwater.urls')),

    # reach
    (r'^metrics/reach/', include('metrics.reach.urls')),

    # recipes
    (r'^metrics/recipes/', include('metrics.recipes.urls')),

    # sales
    (r'^metrics/sales/', include('metrics.sales.urls')),

    # smarts and skills
    (r'^metrics/skills/', include('metrics.skills.urls')),

    # yum and yuck
    (r'^metrics/yumyuck/', include('metrics.yumyuck.urls')),

    # general metrics
    (r'^metrics/', include('metrics.urls')),

    # Estimates
    url(r'^estimates/', include('estimates.urls')),

    # reports
    url(r'^reports/', include(reports.urls.main_patterns)),
    url(r'^gardens/(?P<id>\d+)/report/', include(reports.urls.garden_patterns)),

    # auth
    (r'^accounts/$', 'farmingconcrete.views.account'),
    (r'^accounts/password/reset/$', 'accounts.views.password_reset'),
    (r'^accounts/password/reset/email=(?P<email>.*)$',
     'accounts.views.password_reset'),
    (r'^accounts/registration/',
     include('registration.backends.default.urls')),
    (r'^accounts/', include(accounts.urls.built_in_auth_urls)),

    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Pages
    url(r'^data-collection-toolkit/$', views.flatpage,
        {'url': '/data-collection-toolkit/'}, name='data_collection_toolkit'),

    # miscellany
    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^fc/', include('farmingconcrete.urls')),
    url(r'^djangojs/', include('djangojs.urls')),
    url(r'feedback/success/', TemplateView.as_view(
        template_name='feedback/feedback_success.html'
    ), name='feedback_success'),
    url(r'feedback/', include('feedback.urls')),

    (r'^harvestmap/$', 'harvestmap.views.map'),
    (r'^harvestmap/gardens/kml', 'harvestmap.views.kml'),
    (r'^harvestmap/data', 'harvestmap.views.data'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler500 = 'barn.views.server_error'
