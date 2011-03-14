from django.db import models
from django.forms import ModelForm, HiddenInput, ModelChoiceField, TextInput, CharField, DecimalField

from farmingconcrete.models import Garden, Variety
    
class Box(models.Model):
    class Meta:
        verbose_name_plural = 'Boxes'
        ordering = ['name']

    garden = models.ForeignKey(Garden)
    name = models.CharField(
        max_length=32
    )
    length = models.DecimalField(max_digits=4, decimal_places=1)
    width = models.DecimalField(max_digits=4, decimal_places=1)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s), %d x %d" % (self.garden.name, self.name, self.length, self.width)

class Patch(models.Model):
    class Meta:
        verbose_name_plural = 'Patches'
        ordering = ['variety']

    box = models.ForeignKey(Box)
    variety = models.ForeignKey(Variety)
    plants = models.IntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        area = self.area
        if not area:
            area = 0
        return "%s (%s), %s: %d (plants), %d (area)" % (self.box.garden.name, self.box.name, self.variety, self.plants, area)

class GardenForm(ModelForm):
    class Meta:
        model = Garden
        exclude = ('gardenid', 'longitude', 'latitude', 'added', 'updated')

class BoxForm(ModelForm):
    garden = ModelChoiceField(label='garden', queryset=Garden.objects.all(), widget=HiddenInput())

    name = CharField(
        max_length=32,
        error_messages={'required': "Please enter a name. If you don't have a name in mind, just number the beds."}
    )
    length = DecimalField(
        max_digits=4,
        decimal_places=1,
        error_messages={'required': "Please enter dimensions. This lets us know how many acres of land are being used in this garden for growing food!"}
    )
    width = DecimalField(
        max_digits=4,
        decimal_places=1,
        error_messages={'required': "Please enter dimensions. This lets us know how many acres of land are being used in this garden for growing food!"}
    )

    class Meta:
        model = Box
        exclude = ('added', 'updated')
        widgets = {
            'length': TextInput(attrs={'size': 5}),
            'width': TextInput(attrs={'size': 5}),
        }

class PatchForm(ModelForm):
    box = ModelChoiceField(label='box', queryset=Box.objects.all(), widget=HiddenInput())

    class Meta:
        model = Patch
        exclude = ('added', 'updated')
        widgets = {
            'plants': TextInput(attrs={'size': 3}),
            'area': TextInput(attrs={'size': 3}),
        }
