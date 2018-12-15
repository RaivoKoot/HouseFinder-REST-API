from geopy.geocoders import GoogleV3
from .address_parser import parse_city

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
#from .secret_keys import *

class PropertyPageScraper():
    BASE_URL = 'https://www.zoopla.co.uk'
    geolocator = GoogleV3('***REMOVED***')

    def __init__(self):
        self.reset_data()

    def reset_data(self):
        self.page_data = dict()
        self.error_code = 'NONE'
        self.address_json = None
        self.address = 'default'

    def parse_images(self, images_container):
        images = []
        for container in images_container:
            image_url = container["src"]

            image = dict()
            image['url'] = image_url
            images.append(image)

        self.page_data['images'] = images

    def parse_price(self, price_container):
        price = price_container.text.replace('pcm','')
        price = price.replace('£','').replace(',','').strip()

        self.page_data['price'] = price

    def parse_title(self, title_container):
        title = title_container.text.strip()

        self.page_data['title'] = title

    # must be called after parse_geocode because of self.address_json
    def parse_address(self):
        city = parse_city(self.address_json)

        if city == 'CITYNOTFOUND':
            self.error_code = 'could not parse city from given address: {}'.format(address)
            return

        self.page_data['postcode'] = 'DUMMY'
        self.page_data['street'] = self.address
        self.page_data['city'] = city


    def parse_geocode(self, address_container):
        address = address_container.text.replace(',','')
        self.address = address

        # geolocate the address
        geolocation = self.geolocate_address(address)
        if geolocation == -1:
            self.error_code = 'could not geocode given address: {}'.format(address)
            return

        self.address_json = geolocation.raw

        # latitude, longitude
        latitude = geolocation.latitude
        longitude = geolocation.longitude

        self.page_data['latitude'] = latitude
        self.page_data['longitude'] = longitude

    def parse_bedrooms(self, bedroom_num_container):
        bedrooms = bedroom_num_container.text
        # gets bedroom number from string using regular expressions
        bedrooms = re.findall('\d+', bedrooms)[0]

        self.page_data['bedrooms'] = bedrooms

    def parse_data(self, images_container, price_container, title_container, address_container, bedroom_num_container):
        self.parse_images(images_container)
        self.parse_price(price_container)
        self.parse_title(title_container)
        self.parse_bedrooms(bedroom_num_container)
        self.parse_geocode(address_container)
        self.parse_address()

    def geolocate_address(self, address):
        location = self.geolocator.geocode(address)

        if location == None:
            return -1


        return location

    def get_html_containers(self, page_soup, url):
        try:
            # get information about property listing
            images_container = page_soup.findAll("img",{"class": "dp-gallery__image"})
            price_container = page_soup.find("p",{"class": "ui-pricing__main-price"})
            title_container = page_soup.find("h1",{"class": "ui-property-summary__title ui-title-subgroup"})
            address_container = page_soup.find("h2",{"class": "ui-property-summary__address"})
            bedroom_num_container = page_soup.find("svg",{"class": "ui-icon icon-bed"}).find_next_sibling("span")

            return [
                images_container,
                price_container,
                title_container,
                address_container,
                bedroom_num_container
                ]
        except:
            self.error_code = 'one of the html elements not found in url {}'.format(url)
            return None

    # returns information about one property listings as a JSON
    # attributes are title, address, price, image_urls, latitude, longitude
    def get_information(self, url_extension):
        self.reset_data()
        url = self.BASE_URL + url_extension

        #open connection and grab page
        uClient = uReq(url)

        # load html content
        page_html = uClient.read()
        uClient.close()

        # get html content as soup
        page_soup = soup(page_html, "html.parser")

        # containers holding the information we want
        containers = self.get_html_containers(page_soup, url)
        if self.error_code != 'NONE':
            return self.page_data

        # extract property information from the containers
        self.parse_data(containers[0],containers[1],containers[2],containers[3],containers[4])

        if self.error_code != 'NONE':
            print(self.error_code)

        self.page_data['property_url'] = url # add listing url

        #import json
        #json_string = json.dumps(data)

        return self.page_data
