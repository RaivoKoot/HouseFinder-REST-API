from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Property, Image, Address
from .serializers import PropertySerializer, ImageSerializer, AddressSerializer
from rest_framework.views import APIView

from .test import bullshit

# Create your views here.
class AddressView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.get_specific()

    serializer_class = PropertySerializer


    def get_queryset(self):
        """
        Optionally restricts the returned Properties,
        by filtering against query parameters in the URL.
        """

        #bullshit()
        queryset = self.queryset

        # gets the parameter values from the request uri
        bedrooms = self.request.query_params.get('bedrooms', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        city = self.request.query_params.get('city', None)
        pictures_min = self.request.query_params.get('num_pictures_min', None)
        bedroom_pics_min = self.request.query_params.get('bedroom_pics_min', None)
        kitchen_pics_min = self.request.query_params.get('kitchen_pics_min', None)
        bathroom_pics_min = self.request.query_params.get('bathroom_pics_min', None)
        livingroom_pics_min = self.request.query_params.get('livingroom_pics_min', None)

        address_comparator = self.request.query_params.get('address_comparator', None)
        max_distance_km = self.request.query_params.get('max_distance_km', None)

        # filters the queryset based off of given parameters
        queryset = queryset.filter_properties(bedrooms, price_min, price_max, \
            city, pictures_min, bedroom_pics_min, kitchen_pics_min, \
            bathroom_pics_min, livingroom_pics_min)

        queryset = queryset.filter_max_distance(address_comparator, max_distance_km)

        return queryset
