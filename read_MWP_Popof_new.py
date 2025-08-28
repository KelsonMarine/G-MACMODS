'''From https://maps.nrel.gov/marine-energy-atlas/data-viewer/download
unit = s, coordinates = 57.7615, -152.39886
data every 3 hours for all of 2010
'''

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Kodiak files/env. inputs/MWP Popof/Kodiak_waves_new.csv")
print(df)
df["Date"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute"]])
df.set_index("Date", inplace = True)
df = df["Peak Period"]
df = df.to_frame()
df.to_parquet("Popof input data/new_MWP_popof.parquet")
plt.scatter(df.index, df)
plt.show()