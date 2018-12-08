from rest_framework import serializers
from .models import Property, Image, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city',
            'street',
            'postcode',
            'lattitude',
            'longitude')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',
            'rating',
            'room_type',
            'furnished')

class PropertySerializer(serializers.ModelSerializer):
    bedroom_pics = serializers.IntegerField()
    kitchen_pics = serializers.IntegerField()
    bathroom_pics = serializers.IntegerField()
    livingroom_pics = serializers.IntegerField()
    exterior_pics = serializers.IntegerField()
    other_pics = serializers.IntegerField()

    class Meta:
        model = Property
        fields = ('url',
            'price',
            'bedrooms',
            'title',
            'fk_address_id',
            'price',
            'furnished',
            'num_pictures',
            'rating',
            'date_listed',
            'timestamp_logged',
            'bedroom_pics',
            'kitchen_pics',
            'bathroom_pics',
            'livingroom_pics',
            'exterior_pics',
            'other_pics',)
