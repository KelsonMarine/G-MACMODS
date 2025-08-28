'''
Near-surface NO3 data from Gulf of Alaska Fjords, 2004, 2010, 2011
from https://www.sciencebase.gov/catalog/item/66edd208d34e0606a9dc3fb2
NO3 concentrations in uM
Code created 6/20/25
'''
import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = 2
df = pd.read_csv("../nitrogen/nitrate_new.csv")
df = df[~pd.isna(df["Diss_NO3"])]
dates = pd.to_datetime(df["DateTime"])
df.index = dates
monthly_avg = df["Diss_NO3"].resample("MS").mean()
print(monthly_avg)
plt.scatter(monthly_avg.index, monthly_avg, s = POINT_SIZE)
plt.show() #irregular time intervals
# df = pd.read_csv("../nitrogen/Nitrogen_2004-2011.csv")
# df = df[~pd.isna(df["date"])]
# df = df[~pd.isna(df["time"])]
# NO3_vals = df[df["nutrient"] == "NO3"]
# datetime_col = NO3_vals["date"] + " " + NO3_vals["time"]
# dates = pd.to_datetime(datetime_col)
# plt.scatter(dates, NO3_vals["uM"], s = POINT_SIZE)
# plt.show() #irregular time intervals