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
    bedroom_pics = serializers.IntegerField(read_only=True)
    kitchen_pics = serializers.IntegerField(read_only=True)
    bathroom_pics = serializers.IntegerField(read_only=True)
    livingroom_pics = serializers.IntegerField(read_only=True)
    exterior_pics = serializers.IntegerField(read_only=True)
    other_pics = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = Property
        fields = (
            'url',
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
            'other_pics',
            'images',
            'address')
