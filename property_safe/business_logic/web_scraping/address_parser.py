DESIRED_TYPES = ['locality', 'postal_town']

def parse_city(location_json):
    components = location_json['address_components']

    for component in components:
        if check_type(component['types'], DESIRED_TYPES):
            return component['long_name']

    return 'CITYNOTFOUND'

def check_type(type_list, desired_types):
    for type in type_list:
        if type in desired_types:
            return True

    return False
