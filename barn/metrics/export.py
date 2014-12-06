from django_tablib import Field


class DynamicQuerysetDatasetMixin(object):

    def __init__(self, *args, **kwargs):
        try:
            self.queryset = self.get_queryset()
        except Exception:
            pass
        super(DynamicQuerysetDatasetMixin, self).__init__(*args, **kwargs)


class MetricDatasetMixin(DynamicQuerysetDatasetMixin):

    def __init__(self, gardens=None, start=None, end=None):
        self.gardens = gardens
        self.start = start
        self.end = end
        self._meta.fields = ['recorded', 'added_by_display',] + self._meta.fields
        self.base_fields.update({
            'added_by_display': Field(attribute='added_by_display', header='added by')
        })
        super(MetricDatasetMixin, self).__init__()

    def get_queryset(self):
        return self.model.get_records(gardens=self.gardens, start=self.start, end=self.end)
