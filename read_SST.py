'''
Sea surface temperature over time
https://coastwatch.pfeg.noaa.gov/erddap/griddap/nceiPH53sstd1day.graph using
coordinates 59.533767, -142.739306 and 58.606030, -139.981523 and years 2000 to 2020
from https://coastwatch.pfeg.noaa.gov/data.html
in degrees Celsius
code created 6/20/25
'''

import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = .1
df = pd.read_csv("../SST/SST_actual_surface.csv", skiprows = [1])
df = df[~pd.isna(df["sea_surface_temperature"])] #only use values that aren't NaN
dates = pd.to_datetime(df["time"])
df.index = dates #reindexes by date
# print(dates)
# SST_2017 = pd.date_range(start = "2017-01-01", end = "2018-01-01", freq = "D")
# SST_interpolated = df["sea_surface_temperature"].resample("D").interpolate(method = "time")
# print(SST_interpolated)

monthly_avg = df["sea_surface_temperature"].resample("MS").mean() #averages the SST monthly and assigns it to month start
plt.scatter(monthly_avg.index, monthly_avg)
plt.show()
monthly_avg_df = monthly_avg.to_frame(name = "sea_surface_temperature")
monthly_avg_df.to_parquet("input data/SST.parquet")


