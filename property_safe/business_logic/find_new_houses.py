from .web_scraping.rentingpage_navigator import request_property_links, request_properties_data
from django.utils import timezone
from ..models import Address, Property, Image

from django.core.exceptions import ObjectDoesNotExist


def post_new_properties_to_database(city):

    city = 'Sheffield'
    property_links = request_property_links(city)

    property_data = request_properties_data(property_links)


# is duplicate if there is another property with the same amount of
# bedrooms where one of its pictures is the same
# returns -1 if there its not a duplicate, the id of the property
# otherwise
def isDuplicate(property):
    image_urls = []
    for image in property['images']:
        image_urls.append(image['url'])

    properties_same_image = Property.objects \
        .has_bedrooms(property['bedrooms']) \
        .filter(images__url__in=image_urls)

    existing_images = properties_same_image.count()

    # there are no properties with the same image
    if existing_images > 0:
        return True

    # There are properties with the same images or not, but if so
    # then they are for marketing them with a different amount of rooms
    return False


# checks if the property's address already exists.
# returns the addresses primary key or posts it and
# then returns the primary key
def postPropertyAddress(property):

    street = property['street']
    city = property['city']
    postcode = property['postcode']
    latitude = property['latitude']
    longitude = property['longitude']

    address_entry = address_exists(street,city,postcode)

    # if it exists
    if address_entry != -1:
        return address_entry

    # if it does not exist, post it and return primary key, which
    # is the return of the post method
    return postAddress(street,city,postcode,latitude,longitude)

def address_exists(street,city,postcode):
    try:
        address_entry = Address.objects.get(street=street, city=city, postcode=postcode)
        return address_entry
    except ObjectDoesNotExist:
        return -1

# posts a new address using the given parameters and returns its pk
def postAddress(street, city, postcode, latitude, longitude):
    address = Address(
                street=street,
                city=city,
                postcode=postcode,
                lattitude=latitude,
                longitude=longitude
                )
    address.save()

    return address

def postPropertyImages(property):
    images = property['images']
    image_entries = []

    for image in images:
        url = image['url']
        image_entry = image_exists(url)

        # if it does not exists
        if image_entry == 'image not yet in database':
            rating = image['rating']
            image_entry = postImage(url, rating)

        image_entries.append(image_entry)

    return image_entries

def image_exists(url):
    try:
        image_entry = Image.objects.get(url=url)
        return image_entry
    except ObjectDoesNotExist:
        return 'image not yet in database'

def postImage(url, rating, room_type='UNKNOWN', furnished='False'):
    image = Image(
                url=url,
                rating=rating,
                room_type=room_type,
                furnished=furnished,
                )
    image.save()

    return image

def postProperty(url, price, bedrooms, title, address_fk,
    furnished, num_pictures, rating, images):

    date_listed = timezone.localdate() #placeholder for now
    timestamp_logged=timezone.now()

    property = Property(
                url=url,
                price=price,
                bedrooms=bedrooms,
                title=title,
                fk_address_id=address_fk,
                furnished=furnished,
                num_pictures=num_pictures,
                rating=rating,
                date_listed=date_listed,
                timestamp_logged=timestamp_logged,
                )
    property.save()

    for image in images:
        property.images.add(image)

# posts the property and all of its related entitites image and address
def postPropertyComplete(property):
    # dont post
    if isDuplicate(property):
        return

    url = property['property_url']
    price = property['price']
    bedrooms = property['bedrooms']
    title = property['title']
    furnished = False #default
    num_pictures = str(len(property['images']))
    rating = property['rating']

    address_fk = postPropertyAddress(property)
    images = postPropertyImages(property)

    postProperty(
        url,
        price,
        bedrooms,
        title,
        address_fk,
        furnished,
        num_pictures,
        rating,
        images
        )
