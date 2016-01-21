from django.contrib import admin
from django.shortcuts import redirect
from django.conf.urls import url

from estimates.models import EstimatedYield, EstimatedCost
from estimates.admin_views import make_yield_estimates


class EstimatedYieldAdmin(admin.ModelAdmin):
    search_fields = ('crop__name',)
    list_display = ('crop', 'estimated', 'garden_type', 'valid_start',
                    'valid_end', 'pounds_per_plant', 'notes', 'should_be_used')
    list_filter = ('estimated', 'should_be_used', 'garden_type', 'crop')

    def make_yield_estimates_success(self, request):
        """Message user, redirect back to list"""
        self.message_user(request, "Successfully created new Estimated yields.")
        opts = self.model._meta
        return redirect('admin:%s_%s_changelist' % (
            opts.app_label, opts.object_name.lower()
        ))

    def get_urls(self):
        opts = self.model._meta
        app_label, object_name = (opts.app_label, opts.object_name.lower())
        prefix = "%s_%s" % (app_label, object_name)

        urls = super(EstimatedYieldAdmin, self).get_urls()
        my_urls = [
            url(r'^makeall/$', make_yield_estimates, name='%s_makeall' % prefix),
            url(r'^makeall/success/$', self.make_yield_estimates_success,
                name='%s_makeall_success' % prefix),
        ]
        return my_urls + urls


class EstimatedCostAdmin(admin.ModelAdmin):
    search_fields = ('crop__name',)
    list_display = ('crop', 'estimated', 'valid_start', 'valid_end',
                    'cost_per_pound', 'source', 'notes', 'organic',
                    'should_be_used')
    list_filter = ('estimated', 'source', 'should_be_used', 'crop')


admin.site.register(EstimatedYield, EstimatedYieldAdmin)
admin.site.register(EstimatedCost, EstimatedCostAdmin)
