
class WebScraper():

    def __init__(self):
        self.BASE_URL = 'https://www.zoopla.co.uk/to-rent/property/city/?added=1_hours&price_frequency=per_month&q=city&results_sort=newest_listings&search_source=to-rent&page_size=100'
        self.page_number_code = "&pn=00"

    def assembleUrl(self, city):
        #BASE_URL = 'https://www.zoopla.co.uk/to-rent/property/city/?added=4_hours&price_frequency=per_month&q=city&results_sort=newest_listings&search_source=to-rent'
        #BASE_URL = 'https://www.zoopla.co.uk/to-rent/property/city/?price_frequency=per_month&q=city&results_sort=newest_listings&search_source=to-rent&page_size=100'

        url = self.BASE_URL.replace('city', city)
        url += self.page_number_code

        return url

    def getNextPageUrl(self, url):
        url = url[:-2] #remove last two digits which are the page number
        url += str(self.page_counter).zfill(2)

        return url

    # gets all the links of all ads if you were to search zoopla for all properties
    # in a specific city.
    def request_property_links(self, city):
        from .webscrape_properties_findlinks import scrape_property_links
        self.page_counter = 1

        ad_links = []
        zooplasearch_url = self.assembleUrl(city)

        # iterations collect links from a rental seach on zoopla from
        # page one to the last that has no listing on it

        # each loop goes through one page of house listings. Loop n+1 checks
        # the next page of listings. Runs until it arrives at the last page which
        # does not have any listings on it anymore.
        while True:
            zooplasearch_url = self.getNextPageUrl(zooplasearch_url)
            new_links = scrape_property_links(zooplasearch_url)

            # once no more links are found we have finished our search
            if(len(new_links) == 0):
                break

            ad_links += new_links

            print('Links of page {} have been found. A total of {} links now'.format(self.page_counter, len(ad_links)))
            self.page_counter += 1

        # reverse so that the newest listing gets posted last into database
        ad_links.reverse()
        return ad_links

    # takes in a list of links to properties. Return a list of dictionaries
    # each containing data about a property
    def request_properties_data(self, property_links):
        from .webscrape_properties_parsedata import PropertyPageScraper
        page_scraper = PropertyPageScraper()

        counter = 0
        propertydata_list = []
        for property_link in property_links:

            try:
                page_scraper.reset_data()
                property_data = page_scraper.get_information(property_link)

                if page_scraper.error_code == 'NONE':
                    propertydata_list.append(property_data)
                else:
                    print(page_scraper.page_data)
                    print(page_scraper.error_code)

            except Exception as exception:
                print(exception)


            counter += 1
            print('scraped data of property {} of {}'.format(counter, len(property_links)))



        return propertydata_list
