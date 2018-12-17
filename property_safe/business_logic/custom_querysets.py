from django.db.models.query import QuerySet
from django.db.models import Count, Q, Prefetch
from .location_comparison import DistanceCalculator

class AddressQuerySet(QuerySet):
    def has_street(self, street):
        return self.filter(street__exact=street)

    def in_city(self, city):
        return self.filter(city__exact=city)

    def has_postcode(self, postcode):
        return self.filter(postcode__exact=postcode)

    def get_specific_address(self, street, city, postcode):
        return self.has_street(street).in_city(city).has_postcode(postcode)

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

    def has_bedrooms(self, num_bedrooms):
        return self.filter(bedrooms=num_bedrooms)

    def in_city(self, city):
        return self.filter(fk_address_id__city__exact=city)

    def min_price(self, price_min):
        return self.filter(price__gte=price_min)

    def max_price(self, price_max):
        return self.filter(price__lte=price_max)

    def min_pictures(self, pictures_min):
        return self.filter(num_pictures__gte=pictures_min)

    def min_bedroom_pics(self, bedroom_pics_min):
        return self.filter(bedroom_pics__gte=bedroom_pics_min)

    def min_kitchen_pics(self, kitchen_pics_min):
        return self.filter(kitchen_pics__gte=kitchen_pics_min)

    def min_bathroom_pics(self, bathroom_pics_min):
        return self.filter(bathroom_pics__gte=bathroom_pics_min)

    def min_livingroom_pics(self, livingroom_pics_min):
        return self.filter(livingroom_pics__gte=livingroom_pics_min)

    # filters queryset by a bunch of parameters
    def filter_properties(self, bedrooms, price_min, price_max, city, \
        pictures_min, bedroom_pics_min, kitchen_pics_min, bathroom_pics_min, \
        livingroom_pics_min):

        # filter for bedrooms
        if bedrooms is not None:
            self = self.has_bedrooms(bedrooms)
        # filter for city
        if city is not None:
            self = self.in_city(city)
        # filter for price
        if price_min is not None:
            self = self.min_price(price_min)
        # filter for price
        if price_max is not None:
            self = self.max_price(price_max)

        # filter for picture amount
        if pictures_min is not None:
            self = self.min_pictures(pictures_min)
        # filter for bedroom pictures
        if bedroom_pics_min is not None:
            self = self.min_bedroom_pics(bedroom_pics_min)
        # filter for kitchen pictures
        if kitchen_pics_min is not None:
            self = self.min_kitchen_pics(kitchen_pics_min)
        # filter for bathroom pictures
        if bathroom_pics_min is not None:
            self =self.min_bathroom_pics(bathroom_pics_min)
        # filter for livingroom pictures
        if livingroom_pics_min is not None:
            self = self.min_livingroom_pics(livingroom_pics_min)

        return self

    def get_top_x_results(self, x):
        return self[:x]

    def order(self):
        return self.order_by('-rating')#.order_by('-timestamp_logged')


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
        geo_locator = DistanceCalculator()
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
