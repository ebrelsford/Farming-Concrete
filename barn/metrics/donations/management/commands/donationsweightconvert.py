from django.core.management.base import BaseCommand

from pint import UnitRegistry

from ...models import Donation

ureg = UnitRegistry()


class Command(BaseCommand):
    help = 'Convert old-style donation weights to new-style'

    def handle(self, *args, **options):
        records = Donation.objects.filter(
            pounds__isnull=False,
            weight__isnull=True
        )
        for record in records:
            # weight is currently in pounds, fix that
            record.weight = (record.pounds * ureg.pound).to(ureg.gram).magnitude
            record.save()
