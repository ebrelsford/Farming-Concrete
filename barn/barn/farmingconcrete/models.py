from django.db import models

class GardenType(models.Model):
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=32)

class Garden(models.Model):
    name = models.CharField('garden name', max_length=512)
    type = models.ForeignKey(GardenType)
    gardenid = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField('garden address', max_length=64)

    BOROUGH_CHOICES = (
        ('Brooklyn', 'Brooklyn'),
        ('Bronx', 'Bronx'),
        ('Manhattan', 'Manhattan'),
        ('Queens', 'Queens'),
        ('Staten Island', 'Staten Island'),
    )
    borough = models.CharField(max_length=32, choices=BOROUGH_CHOICES)
    neighborhood = models.CharField(max_length=64)
    zip = models.CharField(max_length=16)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('can_edit_any_garden', 'Can edit any garden'),
        )

    def __unicode__(self):
        return self.name

    @staticmethod
    def counted():
        return Garden.objects.exclude(box=None)

    @staticmethod
    def uncounted():
        return Garden.objects.filter(box=None)

class Variety(models.Model):
    class Meta:
        verbose_name_plural = 'Varieties'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=64)
