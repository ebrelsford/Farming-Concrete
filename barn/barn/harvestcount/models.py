from django.db import models
from django.forms import ModelForm, HiddenInput, ModelChoiceField, TextInput, CharField, DecimalField

from ajax_select.fields import AutoCompleteSelectField

from audit.models import AuditedModel
from farmingconcrete.models import Garden, Variety

class Gardener(AuditedModel):
    garden = models.ForeignKey(Garden)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

class Harvest(AuditedModel):
    gardener = models.ForeignKey(Gardener)
    variety = models.ForeignKey(Variety)

    weight = models.DecimalField(max_digits=6, decimal_places=2)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    harvested = models.DateTimeField()

class HarvestForm(ModelForm):
    gardener = ModelChoiceField(label='gardener', queryset=Gardener.objects.all())
    variety = AutoCompleteSelectField('variety', required=True)

    class Meta:
        model = Harvest
        exclude = ('added',)

class GardenerForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(), widget=HiddenInput())

    class Meta:
        model = Gardener
