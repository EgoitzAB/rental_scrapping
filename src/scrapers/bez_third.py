import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

""" The second scrapper who get the rents from bezrealitky in Prague to add in
one index and display """

#The api urls and the list to work with their
urls = ['https://api.bezrealitky.cz/sitemap_en/sitemap_detail_1.xml',
 'https://api.bezrealitky.cz/sitemap_en/sitemap_detail_2.xml']
praha_flats, titles, listings, layouts, ad_links, avalaible_data, meters,\
prices, basic_rents, utilities = [], [], [], [], [], [], [], [], [], []

def bezrealitky_rentals():
    #For loop who iterates over urls, get a response object and append links to list
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        links = soup.find_all('url')
        for link in links:
            try:
                url = link.find('loc').text
                description = link.find('image:title').text
                praha = re.search(r'rent.*praha', description.lower())
                if praha:
                    praha_flats.append(url)
            except:
                pass
    #For loop who iterates over the links and append to lists the needed data
    for flat in praha_flats:
        try:
            r = requests.get(flat)
            soup = BeautifulSoup(r.text, "lxml")
            title = soup.find('span', {'class': 'PropertyAttributes_propertyAttributesItem__kscom'}).a
            title = title.text
            parameters = soup.find('div', {'class' : 'ParamsTable_paramsTableGroup__IIJ_u'})
            listing_ID = parameters.find('tr').text
            layout = parameters.find('tr').next_sibling.td.text
            link = parameters.find('tr').next_sibling.find('a', href=True)
            link = link['href']
            avalaible_from = parameters.find('tr').next_sibling.next_sibling.td.text
            parameters_1 = parameters.next_sibling
            meter = parameters_1.find('tr').td.text
            price_info = soup.find('div', {'class' : 'box ContentBox_contentBox__77m46 contentBox mb-last-0 mb-5 px-5 py-6 p-xl-12 bg-white Box_box--rounded-lg__kF_Xt'})
            price = price_info.find('strong').text
            basic_rent = price_info.find('table', {'class' : 'PriceTable_priceTable__voQsR priceTable'}).td.text
            utility_fees = price_info.find('table', {'class' : 'PriceTable_priceTable__voQsR priceTable'}).tr.next_sibling.strong.text
            if title != None:
                titles.append(title)
            else:
                title.append('N/A')
            if listing_ID != None:
                listings.append(listing_ID)
            else:
                listings.append('N/A')
            if layout != None:
                layouts.append(layout)
            else:
                layouts.append('N/A')
            if link != None:
                ad_links.append(link)
            else:
                ad_links.append('N/A')
            if avalaible_from != None:
                avalaible_data.append(avalaible_from)
            else:
                avalaible_data.append('N/A')
            if meter != None:
                meters.append(meter)
            else:
                meters.append('N/A')
            if price != None:
                prices.append(price)
            else:
                prices.append('N/A')
            if basic_rent != None:
                basic_rents.append(basic_rent)
            else:
                basic_rents.append('N/A')
            if utilities != None:
                utilities.append(utility_fees)
            else:
                utilities.append('N/A')
        except:
            pass

    #Part who create a pandas dataframe to deploy
    df_bez = pd.DataFrame({'Title': titles, 'Layout': layouts,
                           'Available_from': avalaible_data,
                           'Meters': meters, 'Price_rental': prices,
                           'Monthly_fee': utilities, 'Link': ad_links
                          })

    df_bez.to_excel('bezrealitky_first_attemp.xlsx', index=False)
    return df_bez
