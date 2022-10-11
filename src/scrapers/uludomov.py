import requests
import pandas as pd

"""I create the first part of this scrapping exercise, I want to get three
functions who scrappe the most used rental pages of Prague, for the day that one
friend need to get new department to live"""

# make variables to store the scrapped data
title = []
price_rental = []
price_commission = []
price_deposit = []
price_monthly_fee = []
meters = []
district = []
street = []
available_from = []
link = []
# make a function who scrape the modified curl
def ulu_rentals():
    # loop for get all the apartments with te requirements
    for x in range(1, 30):
        cookies = {
            'visitorId': 'c0da1df8-ed19-4f8f-ac2e-943aafcdedb7',
            'ssupp.vid': 'viVd4JAS4b7ct',
            'ssupp.visits': '1',
            'nette-samesite': '1',
            'PHPSESSID': 'de9b3192833d1173b081986495879170',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'Access-Control-Allow-Credentials': 'true',
            'Origin': 'https://www.ulovdomov.cz',
            'Connection': 'keep-alive',
            'Referer': 'https://www.ulovdomov.cz/vyhledavani/pronajem/Praha?cena-do=12000-kc&bounds=50.177403%3B14.706795%3B49.941936%3B14.224453',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'visitorId=c0da1df8-ed19-4f8f-ac2e-943aafcdedb7; ssupp.vid=viVd4JAS4b7ct; ssupp.visits=1; nette-samesite=1; PHPSESSID=de9b3192833d1173b081986495879170',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'DNT': '1',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        json_data = {
            'acreage_from': '',
            'acreage_to': '',
            'added_before': '',
            'banner_panel_width_type': 480,
            'bounds': {
                'north_east': {
                    'lat': 50.177403,
                    'lng': 14.7067945,
                },
                'south_west': {
                    'lat': 49.9419363,
                    'lng': 14.2244533,
                },
            },
            'conveniences': [],
            'dispositions': [],
            'furnishing': [],
            'is_price_commision_free': None,
            'limit': 600,
            'offer_type_id': None,
            'page': str(x), # changed to go across pages
            'price_from': '',
            'price_to': '25000',# need until 22000, better to 25000
            'query': '',
            'sort_by': 'price:asc',
            'sticker': None,
        }
        # post requests with cookies, headers and data and create json object
        response = requests.post('https://www.ulovdomov.cz/fe-api/find', cookies=cookies, headers=headers, json=json_data)
        response_json = response.json()
        # for loop to get the required data
        for i in range(1, len(response_json['offers'])):
            price_rental.append(response_json['offers'][i]['price_rental'])
            price_commission.append(response_json['offers'][i]['price_commission'])
            price_deposit.append(response_json['offers'][i]['price_deposit'])
            available_from.append(response_json['offers'][i]['available_from'])
            price_monthly_fee = response_json['offers'][i]['price_monthly_fee']
            meters.append(response_json['offers'][i]['acreage'])
            street.append(response_json['offers'][i]['street']['label'])
            district.append(response_json['offers'][i]['village_part']['label'])
            title.append(response_json['offers'][i]['seo'])
            link.append(response_json['offers'][i]['absolute_url'])
        # make a dataframe in pandas and send to excel file
        df_ulu = pd.DataFrame({'Title': title, 'Available_from': available_from,
                               'Meters': meters,'Price_rental': price_rental,
                               'Monthly_fee': price_monthly_fee,
                               'Deposit': price_deposit,
                               'Commission': price_commission, 'Link': link
                               })
        df_ulu.to_excel('uludomov_first_attemp.xlsx', index=False)
        return df_ulu
ulu_rentals()
