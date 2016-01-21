from django.core.management.base import BaseCommand

from pint import UnitRegistry

from ...models import LandfillDiversionWeight

ureg = UnitRegistry()


class Command(BaseCommand):
    help = 'Convert old-style landfill diversion weights to new-style'

    def handle(self, *args, **options):
        records = LandfillDiversionWeight.objects.filter(
            weight__isnull=False,
            weight_new__isnull=True
        )
        for record in records:
            # weight is currently in pounds, fix that
            record.weight_new = (record.weight * ureg.pound).to(ureg.gram).magnitude
            record.save()
