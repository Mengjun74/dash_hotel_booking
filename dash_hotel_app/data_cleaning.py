import pandas as pd
from datetime import datetime

# Read the data and clean it
def data_clean(link = "data/hotel_bookings.csv"):
  data = pd.read_csv(link)

  data = data.dropna(subset=['country'])

  data.loc[data['country'].isin(['United States']), 'country'] = 'United States of America'
  data.loc[data['country'].isin(['Czechia']), 'country'] = 'Czech Republic'
  data.loc[data['country'].isin(['Bosnia & Herzegovina']), 'country'] = 'Bosnia and Herzegovina'
  data.loc[data['country'].isin(['Serbia']), 'country'] = 'Republic of Serbia'
  data.loc[data['country'].isin(['North Macedonia']), 'country'] = 'Macedonia'

  # create a combined date column for the arrival date
  data['arrival_date'] = data.apply(lambda x: datetime.strptime(f"{x['arrival_date_year']} {x['arrival_date_month']} {x['arrival_date_day_of_month']}", '%Y %B %d'), axis=1)
  return data


