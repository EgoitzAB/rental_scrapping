import requests
import gzip

from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
from io import BytesIO

""" The third scrapper who get the rents from sreality in Prague is not allowed
in robots.txt, so I will leave the sitemap and structure for who want to crawl """

SITE_URL = "https://www.sreality.cz/sitemap1.xml.gz"
flat_urls = []

def get_cookie(site_url):
    """ Get cookie from a site. """
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    resp = requests.get(site_url, headers=headers)
    cookies = resp.cookies
    return cookies

def get_sitemap(site_url, cookies):
    """ Get sitemap to obtain later the links. """
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "none"
    headers["Sec-Fetch-User"] = "?1"
    headers["Sec-GPC"] = "1"
    headers["DNT"] = "1"
    resp = requests.get(site_url, headers=headers, cookies=cookies)
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

def make_soup(url, cookies):
    """ Get the soup for each link """
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content, 'lxml')
    data = soup.find_all('ul')
    for dat in data:
        print(dat)

if __name__ == '__main__':
    cookies = get_cookie(SITE_URL)
    sitemap = get_sitemap(SITE_URL, cookies=cookies)
    #with open('praha_flat.txt', 'rb') as file:
    #   file = file.read()
    descompress = descompress_sitemap(sitemap)
    flat_url = get_links(descompress)
    for url in flat_url:
        soup = make_soup(url, cookies=cookies)
