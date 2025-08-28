import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Kodiak files/env. inputs/2021_SST_data_kodiak.txt", sep = "\s+", skiprows = [1])
df = df.rename(columns = {"#YY": "year", "MM": "month", "DD": "day", "hh": "hour", "mm": "minute"})
df["Date"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute"]])
df = df.set_index("Date")
plt.plot(df.index, df["WTMP"], label = "2021")


df = pd.read_csv("../../code/Kodiak files/env. inputs/SST_NEW_near_Kodiak_2020.txt", skiprows = [1], delim_whitespace = True)
df = df.rename(columns = {"#YY": "year", "MM": "month", "DD": "day", "hh": "hour", "mm": "minute"})
df["Date"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute"]])
df = df.set_index("Date")
plt.plot(df.index + pd.DateOffset(years = 1), df["WTMP"], label = "2020")





SST_2019 = pd.read_parquet("Popof input data/2019-2019 SST processed.parquet")
SST_2020 = pd.read_parquet("Popof input data/2020-2020 SST processed.parquet")
SST_2021 = pd.read_parquet("Popof input data/2021-2021 SST processed.parquet")
plt.plot(SST_2021.index, SST_2021["WTMP"], label = "new buoy 2021")
plt.plot(SST_2020.index + pd.DateOffset(years = 1), SST_2020["WTMP"], label = "new buoy 2020")
plt.plot(SST_2019.index + pd.DateOffset(years = 2), SST_2019["WTMP"], label = "new buoy 2019")
plt.legend()
plt.title("temperature degrees C over time")
plt.savefig("../../code/model comparisons/temperature 2019-20 vs 2020-21.png")
plt.show()