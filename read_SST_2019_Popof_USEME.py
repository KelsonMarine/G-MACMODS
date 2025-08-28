#uses data from read_SST_NOAA_buoy_KDAA_data.py
import pandas as pd
import os
print(os.getcwd())
df = pd.read_parquet("Popof input data/kdaa2_2019_2019.parquet")
df = df[df["WTMP"] != 999.0]
df = df[df["WTMP"] != 99.0]
df = df["WTMP"]
df = df.to_frame()
#df.to_csv("../DEB model/SST_2019_NOAA.csv")#for DEB model
df.to_parquet("Popof input data/2019-2019 SST processed.parquet")#for G-MACMODS