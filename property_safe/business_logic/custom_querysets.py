from django.db.models.query import QuerySet
from django.db.models import Count, Q, Prefetch

class PropertyQuerySet(QuerySet):
    def get_specific(self):
        return self.all().annotate(bedroom_pics=Count('images', filter=Q(images__room_type__exact='bedroom'))) \
                .annotate(kitchen_pics=Count('images', filter=Q(images__room_type__exact='kitchen'))) \
                .annotate(bathroom_pics=Count('images', filter=Q(images__room_type__exact='bathroom'))) \
                .annotate(livingroom_pics=Count('images', filter=Q(images__room_type__exact='living room'))) \
                .annotate(exterior_pics=Count('images', filter=Q(images__room_type__exact='exterior'))) \
                .annotate(other_pics=Count('images', filter=Q(images__room_type__exact='other'))) \
                .prefetch_related('images') \
                .prefetch_related(Prefetch('fk_address_id', to_attr='address'))

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

    def filter_max_distance(self, center_address, max_distance_km):
        pass
