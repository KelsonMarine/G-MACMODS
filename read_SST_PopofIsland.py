'''Sea surface temperature data from buoy 46080 (buoy mentioned in prj_AM_UAF/Metocean_UAF/ndbc) in 2020
from https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc.html
with lat, long, time, and sea_surface_temperature inputs. Found average SST over
daily period for one year, plotted against time.'''


SAMPLED_YEAR = 2020
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
# url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/46080/46080h2020.nc'
# ds = xr.open_dataset(url)
# df = ds["sea_surface_temperature"].isel(latitude = 0, longitude = 0).to_dataframe().reset_index()
# df["time"] = pd.to_datetime(df["time"])
# df = df.set_index("time")
# df_2020 = df[df.index.year == SAMPLED_YEAR]
# SST_daily_2020 = df_2020["sea_surface_temperature"].resample("D").mean()
# SST_daily_2020 = SST_daily_2020.to_frame()
# SST_daily_2020.loc[pd.Timestamp("2020-12-31"), "sea_surface_temperature"] = SST_daily_2020.loc[pd.Timestamp("2020-01-01"), "sea_surface_temperature"]
# SST_daily_2020.to_parquet("Popof input data/SST_popof.parquet")
# print(SST_daily_2020)
# plt.scatter(SST_daily_2020.index, SST_daily_2020)
# plt.show() #temp in degrees C, this plot looks similar to one I saw online, seems accurate
# print(SST_daily_2020["2020-12-10":"2021:01-02"])
SST_df = pd.read_parquet("Popof input data/SST_popof.parquet") #this is missing data after Dec 12 (but I added one point on 12/31)
df_2020 = SST_df[SST_df.index.year == SAMPLED_YEAR]
print(df_2020)
SST_daily_2020 = df_2020["sea_surface_temp"].resample("D").mean().to_frame(name = "sea_surface_temp")
SST_daily_2020.loc[pd.Timestamp("2020-12-31")] = SST_daily_2020.loc[pd.Timestamp("2020-01-01")]
full_index = pd.date_range("2020-01-01", "2020-12-31", freq = "D")
SST_daily_2020 = SST_daily_2020.reindex(full_index)
SST_daily_2020 = SST_daily_2020.interpolate(limit_direction = "both")

SST_daily_2020.to_parquet("Popof input data/SST_popof.parquet")