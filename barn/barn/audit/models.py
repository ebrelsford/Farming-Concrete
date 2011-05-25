from django.db import models
from django.contrib.auth.models import User

class AuditedModel(models.Model):
    """
    A model for which the first and last users to edit it are tracked.
    """

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_added', blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_updated', blank=True, null=True)

    class Meta:
        abstract = True
