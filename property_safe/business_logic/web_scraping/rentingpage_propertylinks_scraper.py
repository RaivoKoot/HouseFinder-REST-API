def scrape_property_links(url):
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup

    #open connection an grab page
    uClient = uReq(url)

    # load html content
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # get all cover_pic_containers. They contain the link to
    # the detailed page of their listing
    property_list_container = page_soup.find("ul",{"class": "listing-results clearfix js-gtm-list"})
    rentlisting_ad_covers = property_list_container.findChildren("a",{"class": "photo-hover"})

    # if page contains no listings anymore it means this is the
    # page after the last page. return an empty array signalizing
    # this is the last page
    if(len(rentlisting_ad_covers) == 0):
        return []

    ad_links = []
    for container in rentlisting_ad_covers:
        ad_link = container["href"]
        ad_links.append(ad_link)

    return ad_links
