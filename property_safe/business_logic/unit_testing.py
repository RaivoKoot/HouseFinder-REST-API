from ..business_logic.find_new_houses import *

def testAddressExists():
    print(address_exists("Nairn Street", "Sheffield", "s10"))
    print(address_exists("Sharrowvale Road", "Sheffield", "s11"))

    print(address_exists("Nairn Street", "Berlin", "s10"))
    print(address_exists("Trash", "City", "s10"))
    print(address_exists("Trash", "City", "random"))

def testPostAddress():
    print(postAddress('ceciliengaerten','Berlin','12159', '55','11'))

def testPostPropAddress():
    data = dict()

    data['street'] = 'ceciliengaerten'
    data['city'] = 'Berlin'
    data['postcode'] = '12159'
    data['latitude'] = '-1'
    data['longitude'] = '-1'

    print(postPropertyAddress(data))

# False
# True
# True
# True
# False
# False
def testIsDuplicate():
    data = dict()

    data['bedrooms'] = 4
    data['image_urls'] = [
            "https://lc.zoocdn.com/2d714fffc16f9a4604ab0af528cb3d03e270fb.jpg",
            "https://lc.zoocdn.com/482324f12e6b55e655304deb303cce76f24a1ac.jpg",
            "https://lc.zoocdn.com/83c17c0186c74540631d1027dcce605157e477f.jpg"
        ]

    print(isDuplicate(data))

    data['bedrooms'] = 4
    data['image_urls'] = [
            "https://lc.zoocdn.com/83c176c0186c74540631d1027dcce605157e477f.jpg"
        ]

    print(isDuplicate(data))

    data['bedrooms'] = 5
    data['image_urls'] = [
            "https://lc.zoocdn.com/2d714faffc16f9a4604ab0aaf528cb3d03e270fb.jpg",
            "https://lc.zoocdn.com/4823234f12e6b55e655304deb303cce76f24a1ac.jpg",
            "https://lc.zoocdn.com/83c176c0186c74540631d1027dcce605157e477f.jpg"
        ]

    print(isDuplicate(data))

    data['bedrooms'] = 5
    data['image_urls'] = [
            "https://lc.zoocdn.com/2d714faffc16f9a4604ab0aaf528cb3d03e270fb.jpg"
        ]

    print(isDuplicate(data))

    data['bedrooms'] = 4
    data['image_urls'] = [
            "https://lc.zoocdn.com/83c176c0186c74540631d1027dcs05157e477f.jpg"
        ]

    print(isDuplicate(data))

    data['bedrooms'] = 9
    data['image_urls'] = [
            "https://lc.zoocdn.com/2d714faffc16f9a4604ab0aaf528cb3d03e270fb.jpg",
            "https://lc.zoocdn.com/4823234f12e6b55e655304deb303cce76f24a1ac.jpg",
            "https://lc.zoocdn.com/83c176c0186c74540631d1027dcce605157e477f.jpg"
        ]

    print(isDuplicate(data))

# pk
# -1
# pk
def testImageExists():
    print(image_exists('https://lc.zoocdn.com/83c176c0186c74540631d1027dcce605157e477f.jpg'))
    print(image_exists('https://lc.zoocdn.com/83c176c0186c7454631d1027dcce605157e477f.jpg'))
    print(image_exists('https://lc.zoocdn.com/2d714faffc16f9a4604ab0aaf528cb3d03e270fb.jpg'))

def testPostPropImages():
    data = dict()
    data['images'] = [
            {'url':"https://lc.zoocdn.com/2d714faffc16f9a4604ab0aaf528cb3d03e270fb.jpg", 'rating': 69},
            {'url':"https://lc.zoocdn.com/4823234f12e6b55e655304deb303cce76f24a1ac.jpg", 'rating': 69},
            {'url':"https://lc.zoocdn.com/83c176c0186c74540631d1027dcce605157e477f.jpg", 'rating': 69},
        ]

    postPropertyImages(data)

    data['images'] = [
            {'url':"heyhey.com", 'rating': 69},
            {'url':"https://lc.zoocdn.com/4823234f12e6b55e655304deb303cce76f24a1ac.jpg", 'rating': 33},
            {'url':"facebook.com",'rating': 2},
        ]

    postPropertyImages(data)

def testPostPropertyComplete():
    data = dict()

    data['images'] = [
            {'url':"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Torbogenblick_April_2007.JPG/400px-Torbogenblick_April_2007.JPG", 'rating': 69},
            {'url':"https://images.justlanded.com/housing_images/Germany_Berlin/For-Rent_Apartments/Ceciliengarten-Berlin-1398604/photo/scaled_6346052_7.jpg", 'rating': 69},
            {'url':"https://c1.staticflickr.com/8/7229/7163509922_b1bfbb8de0_b.jpg", 'rating': 69},
            {'url':"https://c1.staticflickr.com/8/7087/7163512218_6b99560ba0_b.jpg", 'rating': 69},
            {'url':"https://t3.ftcdn.net/jpg/01/72/73/12/240_F_172731258_LkWq4iZFzMQbFISaYk94DYYDw6whOyJZ.jpg", 'rating': 69},
            {'url':"https://www.unterwegsinberlin.de/wp-content/uploads/2015/04/radtour_berlin_schoeneberg_30.jpg", 'rating': 69},
            {'url':"https://www.berlin.de/ba-tempelhof-schoeneberg/_assets/politik-und-verwaltung/aemter/stadtentwicklungsamt/denkmalschutz/08_2012_cg_fassade_mit_erker_0421.jpg", 'rating': 69},
        ]

    data['street'] = 'ceciliengaerten 42'
    data['city'] = 'Berlin'
    data['postcode'] = '12159'
    data['latitude'] = '52.473930'
    data['longitude'] = '13.342390'

    data['property_url'] = 'https://raivokoot.com'
    data['price'] = '900'
    data['bedrooms'] = '3'
    data['title'] = 'My Home'
    data['rating'] = '4'

    postPropertyComplete(data)
