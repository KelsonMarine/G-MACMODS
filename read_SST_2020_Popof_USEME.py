#uses data from read_SST_NOAA_buoy_KDAA2_data.py

import pandas as pd

df = pd.read_parquet("Popof input data/kdaa2_2020_2020.parquet")
df = df[df["WTMP"] != 999.0]
df = df[df["WTMP"] != 99.0]
df = df["WTMP"]
df = df.to_frame()
#df.to_csv("../DEB model/SST_2020_NOAA.csv")#for DEB model
df.to_parquet("Popof input data/2020-2020 SST processed.parquet")