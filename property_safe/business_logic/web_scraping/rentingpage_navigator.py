def assembleUrl(city):
    BASE_URL = 'https://www.zoopla.co.uk/to-rent/property/city/?added=24_hours&price_frequency=per_month&q=city&results_sort=newest_listings&search_source=to-rent'

    #***** parameter url codes *****#
    page_number_code = "&pn=0"

    url = BASE_URL.replace('city', city)
    url += page_number_code

    return url

def getNextPageUrl(url):
    url = list(url) # convert to list to change a single character
    url[-1] = str(int(url[-1]) + 1) # add one to last character of url (page number)

    nextPageUrl = ''.join(url) # convert back to string

    return nextPageUrl

# gets all the links of all ads if you were to search zoopla for all properties
# in a specific city.
def request_property_links(city):
    from rentingpage_propertylinks_scraper import scrape_property_links

    ad_links = []
    zooplasearch_url = assembleUrl(city)

    # iterations collect links from a rental seach on zoopla from
    # page one to the last that has no listing on it

    # each loop goes through one page of house listings. Loop n+1 checks
    # the next page of listings. Runs until it arrives at the last page which
    # does not have any listings on it anymore.
    while True:
        zooplasearch_url = getNextPageUrl(zooplasearch_url)
        new_links = scrape_property_links(zooplasearch_url)

        # once no more links are found we have finished our search
        if(len(new_links) == 0):
            break

        ad_links += new_links

    return ad_links

#
def request_properties_data(property_links):
    from property_info_scraper import PropertyPageScraper
    page_scraper = PropertyPageScraper()

    propertydata_list = []
    for property_link in property_links:
        page_scraper.reset_data()
        property_data = page_scraper.get_information(property_link)

        if page_scraper.error_code == 'NONE':
            propertydata_list.append(property_data)
        else:
            print(page_scraper.error_code)

    return propertydata_list

def requestBatchOfPropertydata(city):


    property_links = request_property_links(city)

    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Links to unique property ads have been successfully retrieved from scraping the web", "1/5", 0)

    property_data = request_ordered_data(property_links)

    ctypes.windll.user32.MessageBoxW(0, "Finished scraping property-details from each ad", "2/5", 0)

    return property_data

'''
if __name__ == "__main__":
    links = request_ad_links()

    from listing_info_scraper import getListingInformationAsJson

    json_string = getListingInformationAsJson(links[0])
    file = open('listing_data.json', 'w')
    file.write(json_string)
'''
