'''
Average Wave Period in Cape Edgecumbe Buoy, AK
https://portal.aoos.org/#metadata/13792/station/216/sensor
in unit of seconds
code created 6/20/25
'''

import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = .1
df = pd.read_csv("../avg wave period/avg wave period.csv", skiprows = [1]) #removes row w/ UTC and s that messes with type
df = df[~pd.isna(df["sea_surface_wave_mean_period"])]
dates = pd.to_datetime(df["time"])
df.index = dates #reindexes on dates (which is in datetime)
monthly_avg = df["sea_surface_wave_mean_period"].resample("MS").mean()
print(monthly_avg)
plt.scatter(monthly_avg.index, monthly_avg, s = POINT_SIZE)#hourly data with some missing dates
plt.show()#I believe the strange look of the right side is due to a lack of data from ~2020 on
monthly_avg_df = monthly_avg.to_frame(name = "sea_surface_wave_mean_period")
monthly_avg_df.to_parquet("input data/MWP.parquet")
