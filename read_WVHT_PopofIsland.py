'''Wave height data from buoy 46080 in 2020
from https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc.html
with lat, long, time, and wave_height inputs. Found average wave height over
daily period for one year, plotted against time'''

SAMPLED_YEAR = 2020
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc'
ds = xr.open_dataset(url)
df = ds["wave_height"].isel(latitude = 0, longitude = 0).to_dataframe().reset_index()
df["time"] = pd.to_datetime(df["time"])
df = df.set_index("time")
WVHT = df["wave_height"].values
df_2020 = df[df.index.year == SAMPLED_YEAR]
daily_WVHT_2020 = df_2020["wave_height"].resample("D").mean() #wvht in meters
daily_WVHT_2020 = daily_WVHT_2020.to_frame()
daily_WVHT_2020.loc[pd.Timestamp("2020-12-31"), "wave_height"] = daily_WVHT_2020.loc[pd.Timestamp("2020-01-01"), "wave_height"]
daily_WVHT_2020.to_parquet("Popof input data/WVHT_popof.parquet")
print(daily_WVHT_2020)
plt.scatter(daily_WVHT_2020.index, daily_WVHT_2020)
plt.show() #waves between 0 and 6 meters with a few outliers

