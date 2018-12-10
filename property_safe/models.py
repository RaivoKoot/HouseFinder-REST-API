from django.db import models
from django.utils import timezone
from django.db.models import Count, Q, Prefetch
from .business_logic.custom_querysets import PropertyQuerySet

# Create your models here.

class Address(models.Model):
    postcode = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    lattitude = models.DecimalField(decimal_places=8,max_digits=10)
    longitude = models.DecimalField(decimal_places=8,max_digits=11)

    def __str__(self):
        return self.street + ' ' + self.city + ' ' + self.postcode

class Image(models.Model):
    url = models.URLField(primary_key=True)
    rating = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=30)
    furnished = models.BooleanField()

    def __str__(self):
        return self.url

class Property(models.Model):
    url = models.URLField()
    price = models.FloatField()
    bedrooms = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=50)
    fk_address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    furnished = models.BooleanField()
    num_pictures = models.PositiveSmallIntegerField()
    rating = models.DecimalField(decimal_places=3,max_digits=5)
    date_listed = models.DateField()
    timestamp_logged = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField(Image)

    objects = PropertyQuerySet.as_manager()

    def __str__(self):
        return self.title + ' | ' + str(self.price)
