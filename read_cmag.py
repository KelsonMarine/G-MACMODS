'''
Speeds of currents in Sitka Sound over time
https://tidesandcurrents.noaa.gov/cdata/DataPlot?id=SEA0409&bin=1&bdate=20040508&edate=20040509&unit=1&timeZone=UTC&view=data
using approx depth 33.62m and April 28, 2004 to May 27, 2004
speeds in knots
code created 6/23/25
'''
# if you want this to be for a bigger time frame than ~1 month, get more data from that site and concatenate
import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = 3
df = pd.read_csv("../cmag/cmag_sitka_sound_april-may2004.csv")
df["Date/Time (UTC)"] = pd.to_datetime(df["Date/Time (UTC)"])
df.set_index("Date/Time (UTC)", inplace = True)
monthly_avg = df.resample("ME").mean() #avg of data points from the same hour
print(monthly_avg)
monthly_avg["Speed (m/s)"] = monthly_avg["Speed (knots)"] * 0.514444 #converts from knots to m/s
plt.scatter(monthly_avg.index, monthly_avg["Speed (m/s)"], s = POINT_SIZE)
plt.show() #hourly data
monthly_avg.to_parquet("input data/cmag.parquet")