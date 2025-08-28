'''use read_par_1 instead, because it removes repetition and uses averages'''

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("../par (light at surface)/par sciencebase.gov.csv")
print(df.head())
print(df.shape)
print(df["station"].unique())
print((df["station"] == "G149").sum())#G149 is the name of a buoy
for station in df["station"].unique():
    print(station)
    print((df["station"] == station).sum())
df["datetime"] = df["date"] + " " + df["time"]
dates = pd.to_datetime(df["datetime"])
print(dates)
print(dates.unique())
plt.scatter(dates, df["Par"])
plt.show()

