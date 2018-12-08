from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Property, Image, Address
from .serializers import PropertySerializer, ImageSerializer, AddressSerializer
from rest_framework.views import APIView

from django.db.models import Count
from django.db.models import Q

# Create your views here.
class AddressView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.all() \
                .annotate(bedroom_pics=Count('images', filter=Q(images__room_type__exact='bedroom'))) \
                .annotate(kitchen_pics=Count('images', filter=Q(images__room_type__exact='kitchen'))) \
                .annotate(bathroom_pics=Count('images', filter=Q(images__room_type__exact='bathroom'))) \
                .annotate(livingroom_pics=Count('images', filter=Q(images__room_type__exact='living room'))) \
                .annotate(exterior_pics=Count('images', filter=Q(images__room_type__exact='exterior'))) \
                .annotate(other_pics=Count('images', filter=Q(images__room_type__exact='other')))

    serializer_class = PropertySerializer


    def get_queryset(self):
        """
        Optionally restricts the returned Properties,
        by filtering against query parameters in the URL.
        """

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

        # filter for bedrooms
        if bedrooms is not None:
            queryset = queryset.filter(bedrooms=bedrooms)
        # filter for city
        if city is not None:
            queryset = queryset.filter(fk_address_id__city__exact=city)
        # filter for price
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        # filter for price
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)

        # filter for picture amount
        if pictures_min is not None:
            queryset = queryset.filter(num_images__gte=pictures_min)
        # filter for bedroom pictures
        if bedroom_pics_min is not None:
            queryset = queryset.filter(bedroom_pics__gte=bedroom_pics_min)
        # filter for kitchen pictures
        if kitchen_pics_min is not None:
            queryset = queryset.filter(kitchen_pics__gte=kitchen_pics_min)
        # filter for bathroom pictures
        if bathroom_pics_min is not None:
            queryset = queryset.filter(bathroom_pics__gte=bathroom_pics_min)
        # filter for livingroom pictures
        if livingroom_pics_min is not None:
            queryset = queryset.filter(livingroom_pics__gte=livingroom_pics_min)

        return queryset
