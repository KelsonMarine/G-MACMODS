'''
Significant Wave Height Data from Buoy 46076 in 2008 from April-Decmeber
https://www.ndbc.noaa.gov/historical_data.shtml
height in meters
code created 6/20/25'
'''

import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = 1
df = pd.read_table("../SWH/SWH 2008.txt", sep = " +", skiprows = [1])
df2009 = pd.read_table("../SWH/significant wave height 2009.txt", sep = " +", skiprows = [1])
df2010 = pd.read_table("../SWH/SWH_2010.txt", sep = " +", skiprows = [1])
df = pd.concat([df, df2009])
df = pd.concat([df, df2010])
dates = pd.to_datetime(df[["#YY", "MM", "DD", "hh", "mm"]].rename(columns = {"#YY": "year", "MM": "month", "DD": "day", "hh": "hour", "mm": "minute"}))
df.index = dates
monthly_avg = df["WVHT"].resample("MS").mean()
print(monthly_avg)
plt.scatter(monthly_avg.index, monthly_avg, s = POINT_SIZE)
plt.show() #shows data by the minute
monthly_avg_df = monthly_avg.to_frame(name = "WVHT")
monthly_avg_df.to_parquet("input data/SWH.parquet")