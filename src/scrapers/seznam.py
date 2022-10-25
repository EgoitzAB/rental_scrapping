import requests
import gzip

from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
from io import BytesIO

""" The third scrapper who get the rents from sreality in Prague is not allowed
in robots.txt, so I will leave the sitemap and structure for who want to crawl """
site_url = "https://www.sreality.cz/sitemap1.xml.gz"

def get_sitemap(site_url):
    """ Get sitemap to obtain later the links. """
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "lps=eyJfZnJlc2giOmZhbHNlLCJfcGVybWFuZW50Ijp0cnVlfQ.Y06p8A.c3psuSExTI5jn9-Rr05NWsX0hMU; qusnyQusny=qusny; __cc=RHM0a2E5SWNZUGFuOXpocjsxNjY2MTE0MDQ5:QzVmS1Z5MmN2RENER1RFSjsxNjY2MTI4NDQ5; .seznam.cz|sid=id=15137327952714860790|t=1666099652.499|te=1666099708.053|c=449A85009E6C81CAD8B1BE4CD2C139F0; sid=id=15137327952714860790|t=1666099652.499|te=1666099708.053|c=449A85009E6C81CAD8B1BE4CD2C139F0; sid=id=15137327952714860790|t=1666099652.499|te=1666099658.923|c=F26BC42B373E98DF1BC9BD6D3D37330A; cmpredirectinterval=1666704458881; euconsent-v2=CPhCz0APhCz0AD3ACCENClCgAAAAAAAAAATIAAAAAAAA.YAAAAAAAAAAA; szncmpone=0; szncsr=1666100656; seznam.cz|szncmpone=0"
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
    return links

if __name__ == '__main__':
    sitemap = get_sitemap(site_url)
    decompress = descompress_sitemap(sitemap)
    links = get_links(decompress)
    for link in links:
        print(link.text)
