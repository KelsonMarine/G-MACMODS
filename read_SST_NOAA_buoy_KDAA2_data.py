'''You can input any buoy/date pair from the NDBC NOAA website. I am using https://www.ndbc.noaa.gov/station_page.php?station=kdaa2
and it has data every 6 minutes.
created by Alex'''

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd

#https://www.ndbc.noaa.gov/data/historical/stdmet/kdaa2h2019.txt.gz
def make_buoy_url(name, year):
    return f"http://www.ndbc.noaa.gov/data/historical/stdmet/{name}h{year}.txt.gz"

def get_buoy_data(name, year):
    df = pd.read_csv(make_buoy_url(name, year), sep=r"\s+", skiprows = [1])
    date_columns = {
        "#YY": "year",
        "MM": "month",
        "DD": "day",
        "hh": "hour",
        "mm": "minute"
    }
    df = df.rename(columns = date_columns)

    df["DateTime"] = pd.to_datetime(df[list(date_columns.values())])
    df = df.set_index("DateTime")

    return df

def get_buoy_multiple_years(name, start_year, last_year):

    dataframes = [get_buoy_data(name, year) for year in range(start_year, last_year + 1)]

    df = pd.concat(dataframes, axis=0)

    return df


buoy_name = "kdaa2"
start_year = 2020
last_year = 2021

df = get_buoy_multiple_years(buoy_name, start_year, last_year)

print(df)

df.to_parquet(f"Popof input data/{buoy_name}_{start_year}_{last_year}.parquet")
#FOR DEB, do df to csv here and save it to the place where the DEB model reads it in from