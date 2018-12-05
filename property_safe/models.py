from django.db import models
from django.utils import timezone

# Create your models here.

class Address(models.Model):
    postcode = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    lattitude = models.DecimalField(decimal_places=8,max_digits=10)
    longitude = models.DecimalField(decimal_places=8,max_digits=11)

    def __str__(self):
        return self.street +', '+self.postcode+', '+self.city

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

    def __str__(self):
        return self.address + ' | ' + str(self.price)

class Image(models.Model):
    fk_property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.URLField()
    rating = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=30)
    furnished = models.BooleanField()

    def __str__(self):
        return self.room_type + ' of property ' + self.fk_property_id
