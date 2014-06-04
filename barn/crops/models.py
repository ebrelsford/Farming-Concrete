from django.db import models

from audit.models import AuditedModel


class Crop(AuditedModel):
    name = models.CharField(max_length=64)
    needs_moderation = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        permissions = (
            # TODO account for this being renamed
            ('add_crop_unmoderated', 'Can add crops without moderation'),
        )

    def __unicode__(self):
        return self.name


class Variety(AuditedModel):
    crop = models.ForeignKey(Crop)
    name = models.CharField(max_length=64)
    needs_moderation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Varieties'
        ordering = ['name']
        permissions = (
            ('add_variety_unmoderated', 'Can add varieties without moderation'),
        )

    def __unicode__(self):
        return '%s: %s' (self.crop.name, self.name)
