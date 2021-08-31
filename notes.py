# %%
# Imports data for cars and flights. Imports libraries
import pandas as pd 
import numpy as np 
import altair as alt 
import urllib3 
import json
# imports cars
url_cars = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.json"
cars = pd.read_json(url_cars)
# imports flights
url_flights = 'https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json'
http = urllib3.PoolManager()
response = http.request('GET', url_flights)
flights_json = json.loads(response.data.decode('utf-8'))
flights = pd.json_normalize(flights_json)

# %%
# saves file to json
flights.head(5).to_json("practice.json", orient="records")

# %%
# creates dataframe
df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman', np.nan],
                   "toy": [np.nan, 'Batmobile', 'Bullwhip',np.nan],
                   "born": [pd.NaT, pd.Timestamp("1940-04-25"),
                            pd.NaT, pd.NaT],
                    "power": [np.nan, np.nan, np.nan, np.nan]})

# %%
# drops all in dataframe
df.dropna()

# %%
df.dropna(how="all").dropna(how="all",axis=1)

# %%
# inserts mean into the missing values in cars
cars.wt.fillna(cars.wt.mean())

# %%
# creates new updated data
cars2 = cars.assign(
        wt2 = lambda x: x.wt.fillna(x.wt.mean()),
        gear2 = lambda x: x.gear.replace(999, cars.gear.median())
)

# %%
# fills in data in database
cars2.wt.fillna(cars2.wt.mean(),inplace=True)

# %%
cars.gear.replace(999, cars.gear.median())

# %%
# pulls data for s and s2
s = pd.Series([0, 1, np.nan, 3])
s2 = pd.Series([0, 1, np.nan, 3, np.nan, 8, np.nan, 6])

# %%
s.interpolate()
s2.interpolate()

# %%
# Removes na and fills in numbers in series
s2.ffill()

# %%
# how to check for patterns in missing months
pd.crosstab(flights.month, flights.year)

# %%
pd.crosstab(flights.month, flights.airport_code)

# %%
flights.month.value_counts()

# %%
flights.airport_code.value_counts()

# %%
# dataframe to markdwon table
print(flights.tail(5).filter(["year", "month", "airport_code"]).to_markdown())

# %%
# figure out .describe
flights.describe()
# anomalies (-999) spoted in : num_of_delays_late_aircraft, minutes_delayed_nas 

# %%
# add parameters to .describe
flights.describe(exclude=np.number)
# columns missing data - airport_name, month
# num_of_delays_carrier should be numberic, but is having a problem with 1500+

# %%
# check columns to see different data types
flights.info()
# num_of_delays_carrier is an object when it should be numberic

# %%
# combine month and year data
pd.crosstab(flights.month, flights.year)

# %%
# combine airport_code and year data
pd.crosstab(flights.airport_code, flights.airport_name)
# the airport_code is there, but the airport_name is not

# %%
# counts up how many nulls there are in year
flights.year.isnull().sum()

# %%
# checks how many months have n/a
flights_df = pd.DataFrame(flights)
flights_df.query("month == 'n/a'").count()

# %%
pd.crosstab(flights.year.isnull(), flights.minutes_delayed_carrier.isnull())
# %%
# grand question 3
# According to the BTS website the Weather category only accounts for severe weather delays. Other “mild” weather delays are included as part of the NAS category and the Late-Arriving Aircraft category. Calculate the total number of flights delayed by weather (either severe or mild) using these two rules:
        # -30% of all delayed flights in the Late-Arriving category are due to weather.
        # From April to August, 40% of delayed flights in the NAS category are due to weather. The rest of the months, the proportion rises to 65%.
# columns of data needed
        # need num_of_delays_weather, 
        # airport_code, 
        # num_of_flights_total, 
        # num_of_delays_late_aircraft
        # num_of_delays_nas
# missing month n/a will be multiplied by 0.65 assumption
weather = flights.assign(
    severe = lambda x: x.num_of_delays_weather,
    nodla_nona = lambda x: x.num_of_delays_late_aircraft.replace(-999, np.nan),
    mild_late = lambda x: x.nodla_nona.fillna(x.nodla_nona.mean())*0.3
    mild = lambda x: np.where(x.months.isin(["April", "May", "June", "July", "August"]), 
     x.num_of_delays_nas*0.4, 
     x.num_of_delays_nas*0.65
        ),
    weather = # add up stuff
    percent_weather = # calculate percent weather over total
).filter(['airport_code','month','severe','mild', 'mild_late',
    'weather', 'num_of_delays_total', 'percent_weather'])

# %%
# find the amount of nan's in data
flights.isnull().sum()
# %%
