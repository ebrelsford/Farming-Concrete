from django.core.management.base import BaseCommand

from pint import UnitRegistry

from ...models import CompostProductionWeight

ureg = UnitRegistry()


class Command(BaseCommand):
    help = 'Convert old-style compost weights to new-style'

    def handle(self, *args, **options):
        records = CompostProductionWeight.objects.filter(
            weight__isnull=False,
            weight_new__isnull=True
        )
        for record in records:
            # weight is currently in pounds, fix that
            record.weight_new = (record.weight * ureg.pound).to(ureg.gram).magnitude
            record.save()
