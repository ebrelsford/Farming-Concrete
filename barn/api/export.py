from django_tablib import Field

from metrics.export import DynamicQuerysetDatasetMixin


class PublicMetricDatasetMixin(DynamicQuerysetDatasetMixin):

    def __init__(self, filters=None, **kwargs):
        # Save filters for later
        self.filters = filters

        # Update available base fields
        # XXX Not really anonymized here, garden_pk needs obfuscation before
        #  being exported (eg, in the view)

        self.base_fields.update({
            'garden_pk': Field(attribute='garden_pk', header='garden')
        })
        self.base_fields.update({
            'garden_state': Field(attribute='garden_state', header='garden state')
        })
        self.base_fields.update({
            'garden_zip': Field(attribute='garden_zip', header='garden zip code')
        })

        # Update fields to be exported
        self._meta.fields = [
            'recorded',
            'garden_pk',
            'garden_state',
            'garden_zip',
        ] + self._meta.fields

        self._meta.field_order += (
            'recorded',
            'garden_pk',
            'garden_state',
            'garden_zip',
        )

        super(PublicMetricDatasetMixin, self).__init__()

    def get_queryset(self):
        return self.model.objects.filter(self.filters).select_related('garden')

    class Meta:
        field_order = (
            'recorded',
            'garden_pk',
            'garden_state',
            'garden_zip',
        )
