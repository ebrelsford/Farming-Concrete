from django.core.management.base import BaseCommand

from actstream import action

from ....registry import registry


class Command(BaseCommand):
    help = 'Create metric actions for records that already exist'

    def create_action(self, record):
        try:
            action.send(record.added_by, verb='recorded', action_object=record,
                        target=record.garden, timestamp=record.added)
        except AttributeError:
            # Record is missing some attributes. Skip it.
            pass

    def handle(self, *args, **options):
        self.stdout.write('Creating metric actions...')
        for metric_name in registry.keys():
            self.stdout.write(metric_name)
            records = registry[metric_name]['model'].get_records().exclude(added_by=None)
            for record in records:
                self.create_action(record)

        self.stdout.write('Successfully created metric actions')
