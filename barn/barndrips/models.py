from drip.models import Drip

from .drips import BarnGardenDripBase


class BarnGardenDrip(Drip):
    @property
    def drip(self):
        return BarnGardenDripBase(drip_model=self, name=self.name,
                            from_email=self.from_email if self.from_email else None,
                            from_email_name=self.from_email_name if self.from_email_name else None,
                            subject_template=self.subject_template if self.subject_template else None,
                            body_template=self.body_html_template if self.body_html_template else None)
