from drip.models import BaseDripModel

from .drips import (BarnGardenDripBase, HundredRecordDripBase,
                    InactiveGardenDripBase)


class BarnGardenDrip(BaseDripModel):
    @property
    def drip_class(self):
        return BarnGardenDripBase


class BarnHundredRecordDrip(BaseDripModel):
    @property
    def drip_class(self):
        return HundredRecordDripBase


class BarnInactiveGardenDrip(BaseDripModel):
    @property
    def drip_class(self):
        return InactiveGardenDripBase
