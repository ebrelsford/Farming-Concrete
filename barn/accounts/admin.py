from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile
from metrics.registry import registry
from .utils import get_profile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class EnteredDataListFilter(admin.SimpleListFilter):
    title = _('entered data')
    parameter_name = 'entered_data'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        users_entered_data = []
        metric_models = [m['model'] for m in registry.values()]
        for m in metric_models:
            users_entered_data += m.objects.values_list('added_by', flat=True)
        users_entered_data = filter(None, list(set(users_entered_data)))

        if self.value() == 'yes':
            return queryset.filter(pk__in=users_entered_data)
        if self.value() == 'no':
            return queryset.exclude(pk__in=users_entered_data)


class MetricEnteredDataListFilter(admin.SimpleListFilter):
    title = _('metric entered data')
    parameter_name = 'metric_entered_data'

    def lookups(self, request, model_admin):
        def metric_display(metric):
            return '%d.%d %s' % (metric['group_number'], metric['number'],
                                 metric['name'])
        return ((m['name'], metric_display(m)) for m in registry.sorted())

    def queryset(self, request, queryset):
        if self.value():
            metric_model = registry[self.value()]['model']
            users_entered_data = metric_model.objects.values_list('added_by', flat=True)
            users_entered_data = filter(None, list(set(users_entered_data)))
            return queryset.filter(pk__in=users_entered_data)


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'gardens',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   EnteredDataListFilter, MetricEnteredDataListFilter,)

    def gardens(self, instance):
        gardens = get_profile(instance).gardens.all()
        return format_html_join(
            mark_safe('<br />'),
            mark_safe('<a href="{1}">{0}</a>'),
            ((garden, garden.get_absolute_url(),) for garden in gardens),
        )


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
