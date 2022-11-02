#!/usr/bin/python3
from scrapers import uludomov
from scrapers import bez_third
import pandas as pd

def main():
    """ Make one excel with the data of the rentals on Prague """
    ulu = uludomov.main()
    bezrealitky = bez_third.main()
    rent_flats = pd.concat([bezrealitky, ulu])
    rent_flats.to_excel('rent_flats_first.xlsx', index=False)
    return rent_flats

if __name__ == '__main__':
    print(main())
