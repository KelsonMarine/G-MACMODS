'''From https://maps.nrel.gov/marine-energy-atlas/data-viewer/download
unit = meters, coordinates = 57.7615, -152.39886
'''

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Kodiak files/env. inputs/SWH Popof/Kodiak_waves_new.csv")
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute"]])
df.set_index("Date", inplace = True)
df = df["Significant Wave Height"]
df = df.to_frame()
df.to_parquet("Popof input data/new_SWH_popof.parquet")
plt.scatter(df.index, df)
plt.show()