#data for the loaded in CSV comes from here: https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0219960/Data_CODAP/CSV/

import pandas as pd
df = pd.read_csv("../../Desktop/code/DEB model/DIC.csv", skiprows = [1])
df["Year"] =df["Year_UTC"].astype(int)
df["Month"] = df["Month_UTC"].astype(int)
df["Day"] = df["Day_UTC"].astype(int)
df["time_delta"] = pd.to_timedelta(df["Time_UTC"], unit = "D")
df["date"] = pd.to_datetime(df[["Year", "Month", "Day"]])
df["datetime"] = (df["date"] + df["time_delta"].dt.round("1s"))
filtered_df = df[(df["Depth"] <= 20) & (df["DIC"] > 0)]
result = filtered_df[["datetime", "DIC"]]
result = result.set_index("datetime")
result["DIC"] = result["DIC"] / 1000000 #umol to mol
result.to_csv("/Users/gretaholmes/Desktop/code/DEB model/DIC_valid_data.csv")
