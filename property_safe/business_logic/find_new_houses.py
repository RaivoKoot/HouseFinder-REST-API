from .web_scraping.webscrape_properties import WebScraper
from .web_scraping.property_rater import PropertyRater
from django.utils import timezone
from ..models import Address, Property, Image
from django.db import connection

from django.core.exceptions import ObjectDoesNotExist
import pickle
import datetime

def post_new_properties_to_database(city):
    city = 'sheffield'
    properties = scrape_new_property_data(city)

    #properties = load_from_pickle()

    length = len(properties)
    counter = 0

    connection.close()
    rater = PropertyRater()
    for property in properties:

        try:
            duplicate = isDuplicate(property)
            # dont post this property if duplicate already exits in database
            if duplicate == False:
                rater.rate_property(property)
                post_property_including_relationships(property)
            else:
                print('Duplicate of {}'.format(duplicate))
                print(property['property_url'])

        except Exception as exception:
            connection.close() # refresh connection for when mysql connection closes
            print(exception)



        print("Finished property {} of {}".format(counter, length))
        print()
        print()
        counter += 1

# used for debugging
def save_to_pickle(list):
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M oclock")
    filename = 'logged_webscrapings/property_data_' + date_string + '.pickle'

    pickle_file = open(filename, "wb")
    pickle.dump(list, pickle_file)
    pickle_file.close()

# used for debugging
def load_from_pickle():
    pickle_in = open("property_data.pickle","rb")
    data = pickle.load(pickle_in)

    return data

def scrape_new_property_data(city):
    web_scraper = WebScraper()

    property_links = web_scraper.request_property_links(city)

    properties = web_scraper.request_properties_data(property_links)
    save_to_pickle(properties)

    return properties

# posts the property and all of its related entitites image and address
def post_property_including_relationships(property):

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
        pk = properties_same_image.first().pk
        return pk

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

    address_entry = address_exists(latitude,longitude)

    # if it does not exist yet then post it and get the new Address object
    if address_entry == 'address does not exist yet':
        address_entry = postAddress(street,city,postcode,latitude,longitude)

    return address_entry

'''
def address_exists(street,city,postcode):
    try:
        address_entry = Address.objects.get(street=street, city=city, postcode=postcode)
        return address_entry
    except ObjectDoesNotExist:
        return -1
'''

# checks if a given address already exist in database
# and returns the Address object if it does, -1 otherwise
def address_exists(latitude, longitude):
    try:
        address_entry = Address.objects.get(lattitude=latitude, longitude=longitude)
        return address_entry
    except ObjectDoesNotExist:
        return 'address does not exist yet'

# posts a new address entry using the given parameters and returns its pk
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

# for each image of the property, posts a new Image entry
def postPropertyImages(property):
    images = property['images']
    image_entries = []

    for image in images:
        image_entry = post_image(image)

        image_entries.append(image_entry)

    return image_entries

# posts an image if it does not exist already and returns
# the image object
def post_image(image):
    url = image['url']
    image_entry = image_exists(url)

    # if it does not exists
    if image_entry == 'image not yet in database':
        rating = image['rating']
        image_entry = postImage(url, rating)

    return image_entry

# checks if an image already exists in database.
# If it does, returns the Image object
def image_exists(url):
    try:
        image_entry = Image.objects.get(url=url)
        return image_entry
    except ObjectDoesNotExist:
        return 'image not yet in database'

# POSTs an image to database and returns the Image object
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
