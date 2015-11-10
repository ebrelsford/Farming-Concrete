from drip.models import BaseDripModel

from .drips import BarnGardenDripBase


class BarnGardenDrip(BaseDripModel):
    @property
    def drip_class(self):
        return BarnGardenDripBase
