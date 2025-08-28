'''
Photosynthetically Active Radiation data from Glacier Bay, AK
from https://irma.nps.gov/DataStore/Reference/Profile/2313140
PAR in microEinsteins/m^2*sec
code created 6/20/25
'''

import pandas as pd
import matplotlib.pyplot as plt
POINT_SIZE = 1
df = pd.read_csv("../par (light at surface)/PAR_data.csv")
df = df[~pd.isna(df["par"])] #gets valid PAR vals
dates = pd.to_datetime(df["time_stamp"])
df.index = dates #reindexes on dates (which is in datetime)
monthly_avg = df["par"].resample("MS").mean().dropna().sort_index()
print(monthly_avg)
plt.scatter(monthly_avg.index, monthly_avg)
plt.show()
monthly_avg_df = monthly_avg.to_frame(name = "par")
monthly_avg_df.to_parquet("input data/PAR.parquet")