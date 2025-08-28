'''Sea surface temperature data from station 46264, a bit offshore of Kodiak AK.
There is no data after September, but I assumed that's ok because there's no harvesting after then anyways'''

SAMPLED_YEAR = 2021
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("../Kodiak files/env. inputs/2021_SST_data_kodiak.txt", sep = "\s+", skiprows = [1])
df = df.rename(columns = {"#YY": "year", "MM": "month", "DD": "day", "hh": "hour", "mm": "minute"})
df["Date"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute"]])
df = df.set_index("Date")
daily_avg = df["WTMP"].resample("D").mean()
df_daily = daily_avg.to_frame(name = "SST")
full_index = pd.date_range(start = "2021-01-01", periods = 366, freq = "D")
df_daily = df_daily.reindex(full_index)
df_daily.index.name = "Date"
df_daily["SST"] = df_daily["SST"].interpolate()
df_daily.to_parquet("Popof input data/2021_SST_popof.parquet")

plt.scatter(df_daily.index, df_daily["SST"])
plt.show()