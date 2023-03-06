import requests
import gzip

from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
from io import BytesIO

""" The third scrapper who get the rents from sreality in Prague is not allowed
in robots.txt, so I will leave the sitemap and structure for who want to crawl """

SITE_URL = "https://www.sreality.cz/sitemap1.xml.gz"
flat_urls = []
def get_sitemap(site_url):
    """ Get sitemap to obtain later the links. """
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = #insert user agent
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = #insert cookie
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "none"
    headers["Sec-Fetch-User"] = "?1"
    headers["Sec-GPC"] = "1"
    headers["DNT"] = "1"
    resp = requests.get(site_url, headers=headers)
    return resp.content

def descompress_sitemap(site_response):
    """ Get a byte object and decompress to read the links """
    with BytesIO(site_response) as file:
        with gzip.open(file, 'rb') as f:
            file_data = f.read()
            return file_data

def get_links(xml):
    """ Get the links from the page, and leave cause I think that robots.txt
    prohibits the scrapping """
    soup = BeautifulSoup(xml, 'lxml')
    links = soup.find_all('loc')
    links = [link.text for link in links]
    return links

def make_soup(url):
    """ Get the soup for each link """
    response = requests.get(url)
    print(response)

    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)
    data = soup.find_all('ul')
    for dat in data:
        print(dat)


if __name__ == '__main__':
    #sitemap = get_sitemap(SITE_URL)
    with open('praha_flat.txt', 'rb') as file:
        file = file.read()
        descompress = descompress_sitemap(file)
        flat_url = get_links(descompress)
        for url in flat_url:
            soup = make_soup(url)

