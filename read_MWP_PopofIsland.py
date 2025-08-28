'''Mean wave period data from buoy 46080 (buoy mentioned in prj_AM_UAF/Metocean_UAF/ndbc) in 2020
from https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc.html
with lat, long, time, and average_wpd inputs. Found average MWP (mean wave period) over
daily period for one year, plotted against time.'''


SAMPLED_YEAR = 2020
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc'
ds = xr.open_dataset(url)
df = ds["average_wpd"].isel(latitude = 0, longitude = 0).to_dataframe().reset_index()
df["time"] = pd.to_datetime(df["time"])
df = df.set_index("time")
MWP = df["average_wpd"].values #gives mean wave period in nanoseconds (I believe)
df["average_wpd_seconds"] = df["average_wpd"].dt.total_seconds() #gives MWP in seconds
MWP_seconds = df["average_wpd_seconds"]
df_2020 = df[df.index.year == SAMPLED_YEAR] #plots data from only 2020
MWP_daily_2020 = df_2020["average_wpd_seconds"].resample("D").mean()
MWP_daily_2020 = MWP_daily_2020.to_frame()
MWP_daily_2020.loc[pd.Timestamp("2020-12-31"), "average_wpd_seconds"] = MWP_daily_2020.loc[pd.Timestamp("2020-01-01"), "average_wpd_seconds"]
MWP_daily_2020.to_parquet("Popof input data/MWP_popof.parquet")
print(MWP_daily_2020)
plt.scatter(MWP_daily_2020.index, MWP_daily_2020) #plots MWP over time
plt.show()
