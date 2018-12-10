from geopy.geocoders import Nominatim
from geopy.distance import great_circle

# addresses must be passed as a full string of street city postcode
# without commas

class GeoLocator():

    def __init__(self):
        # Nominatim object to geolocate (get lat and long of) addresses
        self.geolocator = Nominatim(user_agent='PropertyFinder')

    # saves the latitude and longitude of address as tuple
    def set_center_address(self, address):
        self.center = self.get_lat_long(address)

    def set_max_distance_km(self, max_distance_km):
        self.max_distance_km = float(max_distance_km)

    # returns the lattitude and longitude of a given address as a tuple
    def get_lat_long(self, address):
        location = self.geolocator.geocode(address)
        return (location.latitude, location.longitude)

    # function great circle calculates the distance between to geolocations
    def distance_between_lat_long(self, lat_long_one, lat_long_two):
        return great_circle(lat_long_one, lat_long_two).km

    # finds distance between a latitude longitude tuple and an address string
    def distance_between(self, lat_long_one, address_two):
        address_two_lat_long = self.get_lat_long
        return self.distance_between_lat_long(lat_long_one, address_two_lat_long)

    # returns true if the given adress is at most as far away from self.center
    # as self.max_distance_km
    def within_max_distance(self, address):
        # gets the distance between self.center and the given address
        distance = self.distance_between_lat_long(self.center, address)

        if distance < self.max_distance_km:
            return True

        return False
