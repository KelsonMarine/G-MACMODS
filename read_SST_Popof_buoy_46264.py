#https://www.ndbc.noaa.gov/station_page.php?station=46264 2020 data from station 46264
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../../code/Kodiak files/env. inputs/SST_NEW_near_Kodiak_2020.txt", skiprows = 1, delim_whitespace = True)

df = df.rename(columns = {"#yr": "year", "mo": "month", "dy": "day", "hr": "hour", "mn": "minute"})
df["Date"] = pd.to_datetime(df[["year", "month", "day", "hour", "minute"]])
df = df.set_index("Date")
daily_avg = df["degC.1"].resample("d").mean()
df_daily = daily_avg.to_frame(name = "SST")
full_index = pd.date_range(start = "2020-01-01", end = "2020-12-31", freq = "h")
df_daily = df_daily.reindex(full_index)
df_daily.index.name = "Date"
df_daily["SST"] = df_daily["SST"].interpolate()
result = df_daily["SST"]
result = result.to_frame()
plt.plot(result.index, result)
plt.show()
print(result.columns)
result.to_parquet("Popof input data/SST_buoy_46264.parquet")