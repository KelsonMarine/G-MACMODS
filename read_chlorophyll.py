'''
Mass concentration of chlorophyll in the Gulf of Alaska
https://portal.aoos.org/#metadata/100704/station/41/sensor/data
in units microg.L-1
code created 6/20/25
'''

import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = 1
df = pd.read_csv("../chlorophyll/gulf-of-alaska-ecosystem-obse-1_7b58_cd6f_6e3c.csv", skiprows = [1])
dates = pd.to_datetime(df["time"])
df.index = dates #reindexes on dates (which is in datetime)
monthly_avg = df["mass_concentration_of_chlorophyll_in_sea_water"].resample("MS").mean()
print(monthly_avg)
plt.scatter(monthly_avg.index, monthly_avg, s = POINT_SIZE)
plt.show() #missing a fair amount of months
df.to_parquet("input data/chlorophyll.parquet")