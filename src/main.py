from scrapers import uludomov
from scrapers import bez_third
import pandas as pd

def main():
    ulu = uludomov.ulu_rentals()
    bezrealitky = bez_third.bezrealitky_rentals()
    rent_flats = pd.concat([bezrealitky, ulu])
    rent_flats.to_excel('rent_flats_first.xlsx', index=False)
    return rent_flats

if __name__ == '__main__':
    print(main())
