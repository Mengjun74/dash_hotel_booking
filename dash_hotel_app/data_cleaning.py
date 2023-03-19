import pandas as pd
import country_converter as coco
import geopandas as gpd
from dateutil import parser
from datetime import datetime

# Read the data and clean it
def data_clean(link = "data/hotel_bookings.csv"):
  data = pd.read_csv(link)

  data = data.dropna(subset=['country'])

  data['country_full_name'] = coco.convert(data['country'], 'ISO3', 'name')

  data.loc[data['country_full_name'].isin(['United States']), 'country_full_name'] = 'United States of America'
  data.loc[data['country_full_name'].isin(['Czechia']), 'country_full_name'] = 'Czech Republic'
  data.loc[data['country_full_name'].isin(['Bosnia & Herzegovina']), 'country_full_name'] = 'Bosnia and Herzegovina'
  data.loc[data['country_full_name'].isin(['Serbia']), 'country_full_name'] = 'Republic of Serbia'
  data.loc[data['country_full_name'].isin(['North Macedonia']), 'country_full_name'] = 'Macedonia'

  # create a combined date column for the arrival date
  data['arrival_date'] = data.apply(lambda x: datetime.strptime(f"{x['arrival_date_year']} {x['arrival_date_month']} {x['arrival_date_day_of_month']}", '%Y %B %d'), axis=1)
  return data


# Read the map polygon data
def map_df(link = "data/countries.geojson")
  countries_json = gpd.read_file(link)
  country_list = countries_json['name'].tolist()
  full_country_df = pd.DataFrame({'country_full_name': country_list})
  return countries_json, full_country_df
