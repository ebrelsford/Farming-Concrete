from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

from farmingconcrete.views import IndexView
import reports.urls

admin.autodiscover()

urlpatterns = [
    url(r'^(?:(?P<year>\d{4})/)?$',
        IndexView.as_view(),
        name='home'
    ),

    url(r'^gardens/', include('farmingconcrete.garden_urls')),
    url(r'^crops/', include('crops.urls')),

    # compost
    url(r'^metrics/compost/', include('metrics.compost.urls')),

    # crop count
    url(r'^metrics/cropcount/', include('metrics.cropcount.urls')),

    # donation
    url(r'^metrics/donations/', include('metrics.donations.urls')),

    # harvest count
    url(r'^metrics/harvestcount/', include('metrics.harvestcount.urls')),

    # landfill diversion
    url(r'^metrics/landfilldiversion/', include('metrics.landfilldiversion.urls')),

    # looking good
    url(r'^metrics/lookinggood/', include('metrics.lookinggood.urls')),

    # moods
    url(r'^metrics/moods/', include('metrics.moods.urls')),

    # participation
    url(r'^metrics/participation/', include('metrics.participation.urls')),

    # rainwater
    url(r'^metrics/rainwater/', include('metrics.rainwater.urls')),

    # reach
    url(r'^metrics/reach/', include('metrics.reach.urls')),

    # recipes
    url(r'^metrics/recipes/', include('metrics.recipes.urls')),

    # sales
    url(r'^metrics/sales/', include('metrics.sales.urls')),

    # smarts and skills
    url(r'^metrics/skills/', include('metrics.skills.urls')),

    # yum and yuck
    url(r'^metrics/yumyuck/', include('metrics.yumyuck.urls')),

    # general metrics
    url(r'^metrics/', include('metrics.urls')),

    # Estimates
    url(r'^estimates/', include('estimates.urls')),

    # reports
    url(r'^reports/', include(reports.urls.main_patterns)),
    url(r'^gardens/(?P<pk>\d+)/report/', include(reports.urls.garden_patterns)),
    url(r'^gardens/group/(?P<pk>\d+)/report/', include(reports.urls.garden_group_patterns)),

    # API
    url(r'^api-admin/', include('adminapi.urls')),
    url(r'^api/', include('api.urls')),

    # auth
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/registration/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Pages
    url(r'^data-collection-toolkit/$', views.flatpage,
        {'url': '/data-collection-toolkit/'}, name='data_collection_toolkit'),

    # miscellany
    url(r'^ajax_select/', include('ajax_select.urls')),
    url(r'^fc/', include('farmingconcrete.urls')),
    url(r'^djangojs/', include('djangojs.urls')),
    url(r'feedback/success/', TemplateView.as_view(
        template_name='feedback/feedback_success.html'
    ), name='feedback_success'),
    url(r'feedback/', include('feedback.urls')),

    url(r'^report_builder/', include('report_builder.urls')),
    url(r'^hijack/', include('hijack.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler500 = 'barn.views.server_error'
