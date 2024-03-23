#!/usr/bin/python3
import requests
import pandas as pd

"""I create the first part of this scrapping exercise, I want to get three
functions who scrappe the most used rental pages of Prague, for the day that one
friend need to get new department to live"""

# variables to store the scrapped data
title, price_rental, price_commission, price_deposit, price_monthly_fee, meters,\
district, street, available_from, link = [], [], [], [], [], [],[], [] ,[], []


def ulu_rentals():
    """ Function who get the data from the uludomov api and return response_json
    object from automatic curl transformation."""

    for x in range(1, 30):
        cookies = {
            #get and insert the cookie
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
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
            # 'Cookie': get the cookie
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
        return response_json

def get_data(response_json):
    """Function who get the required data and append to global lists, to after
    make a pandas dataframe."""

    try:
        for i in range(1, len(response_json['offers'])):
            if response_json['offers'][i]['price_rental']:
                price_rental.append(response_json['offers'][i]['price_rental'])
            else:
                price_rental.append('N/A')
            if response_json['offers'][i]['price_commission']:
                price_commission.append(response_json['offers'][i]['price_commission'])
            else:
                price_commission.append('N/A')
            if response_json['offers'][i]['price_deposit']:
                price_deposit.append(response_json['offers'][i]['price_deposit'])
            else:
                price_deposit.append('N/A')
            if response_json['offers'][i]['available_from']:
                available_from.append(response_json['offers'][i]['available_from'])
            else:
                available_from.append('N/A')
            if response_json['offers'][i]['price_monthly_fee']:
                price_monthly_fee.append(response_json['offers'][i]['price_monthly_fee'])
            else:
                price_monthly_fee.append('N/A')
            if response_json['offers'][i]['acreage']:
                meters.append(response_json['offers'][i]['acreage'])
            else:
                meters.append('N/A')
            if response_json['offers'][i]['street']['label']:
                street.append(response_json['offers'][i]['street']['label'])
            else:
                street.append('N/A')
            if response_json['offers'][i]['village_part']['label']:
                district.append(response_json['offers'][i]['village_part']['label'])
            else:
                district.append('N/A')
            if response_json['offers'][i]['seo']:
                title.append(response_json['offers'][i]['seo'])
            else:
                title.append('N/A')
            if response_json['offers'][i]['absolute_url']:
                link.append(response_json['offers'][i]['absolute_url'])
            else:
                link.append('N/A')
    except:
        pass

def make_df():
    """Function to create pandas dataframe and return it for posterior
    manipulation."""

    df_ulu = pd.DataFrame({'Title': title, 'Available_from': available_from,
                           'Meters': meters,'Price_rental': price_rental,
                           'Monthly_fee': price_monthly_fee,
                           'Deposit': price_deposit,
                           'Commission': price_commission, 'Link': link
                           })
    return df_ulu

def pd_to_excel(df):
    """Function to create a excel sheet from dataframe."""
    return df.to_excel('uludomov_first_attemp.xlsx', index=False)

def main():
    """ Get the data and return excel_file """
    response_json = ulu_rentals()
    get_data(response_json)
    ulu_df = make_df()
    df = make_df()
    pd_to_excel(df)
    return df

if __name__ == '__main__':
    main()
