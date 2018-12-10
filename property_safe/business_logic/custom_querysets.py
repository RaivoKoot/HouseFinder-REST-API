from django.db.models.query import QuerySet
from django.db.models import Count, Q, Prefetch
from .location_comparison import GeoLocator

class PropertyQuerySet(QuerySet):
    def get_specific(self):
        return self.all().annotate(bedroom_pics=Count('images', filter=Q(images__room_type__exact='bedroom'))) \
                .annotate(kitchen_pics=Count('images', filter=Q(images__room_type__exact='kitchen'))) \
                .annotate(bathroom_pics=Count('images', filter=Q(images__room_type__exact='bathroom'))) \
                .annotate(livingroom_pics=Count('images', filter=Q(images__room_type__exact='living room'))) \
                .annotate(exterior_pics=Count('images', filter=Q(images__room_type__exact='exterior'))) \
                .annotate(other_pics=Count('images', filter=Q(images__room_type__exact='other'))) \
                .prefetch_related('images') \
                .prefetch_related(Prefetch('fk_address_id', to_attr='address')) \
                .select_related('fk_address_id')

    # filters queryset by a bunch of parameters
    def filter_properties(self, bedrooms, price_min, price_max, city, \
        pictures_min, bedroom_pics_min, kitchen_pics_min, bathroom_pics_min, \
        livingroom_pics_min):

        # filter for bedrooms
        if bedrooms is not None:
            self = self.filter(bedrooms=bedrooms)
        # filter for city
        if city is not None:
            self = self.filter(fk_address_id__city__exact=city)
        # filter for price
        if price_min is not None:
            self = self.filter(price__gte=price_min)
        # filter for price
        if price_max is not None:
            self = self.filter(price__lte=price_max)

        # filter for picture amount
        if pictures_min is not None:
            self = self.filter(num_images__gte=pictures_min)
        # filter for bedroom pictures
        if bedroom_pics_min is not None:
            self = self.filter(bedroom_pics__gte=bedroom_pics_min)
        # filter for kitchen pictures
        if kitchen_pics_min is not None:
            self = self.filter(kitchen_pics__gte=kitchen_pics_min)
        # filter for bathroom pictures
        if bathroom_pics_min is not None:
            self = self.filter(bathroom_pics__gte=bathroom_pics_min)
        # filter for livingroom pictures
        if livingroom_pics_min is not None:
            self = self.filter(livingroom_pics__gte=livingroom_pics_min)

        return self

    # removes all propertie entries from queryset that are too far
    # away from a specified place (center_address)
    def filter_max_distance(self, center_address, max_distance_km):

        # make sure both parameters were given
        if (center_address is None) or (max_distance_km is None):
            return self

        # query all the entries(only with attributes id and address)
        # from queryset
        property_list = list(self.values('id', 'fk_address_id__lattitude', 'fk_address_id__longitude'))

        # setupt geolocation comparators
        geo_locator = GeoLocator()
        geo_locator.set_center_address(center_address)
        geo_locator.set_max_distance_km(max_distance_km)

        # list will be filled with ids of properties that are too far away
        # (further away than max_distance_km)
        property_ids_to_exclude = []

        # iterate over each property and use properties address to
        # find out if it is within specified max_distnce
        for property in property_list:
            #address = (property.fk_address_id.lattitude, property.fk_address_id.longitude)
            address = (property['fk_address_id__lattitude'], property['fk_address_id__longitude'])
            property_id = property['id']

            # add property id to exclusion list if too far away
            if not geo_locator.within_max_distance(address):
                property_ids_to_exclude.append(property_id)


        # exclude properties from queryset and return it
        return self.exclude(id__in=property_ids_to_exclude)
