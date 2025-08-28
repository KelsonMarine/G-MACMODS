'''Photosynthetically Active Radiation from Anchor Point, AK
https://portal.aoos.org/#metadata/75407/station/data
PAR in units of mmol/m^2 (but another link says mmol/m^2/s). The data varies a lot on a day-to-day basis
but seems to have a regular seasonal trend. It is sampled every 15 minutes, 2014-2025.'''

SAMPLED_YEAR = 2018
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Kodiak files/env. inputs/PAR Popof/PAR-anchor-point-AK.csv", skiprows = [1])
df["time"] = pd.to_datetime(df["time"])
df["time"] = df["time"].dt.tz_localize(None)
df = df.set_index("time")
plt.plot(df.index, df)
plt.show()
df = df["surface_downwelling_photosynthetic_photon_flux_in_air_cm_time__sum_over_pt15m"]
#df_2018 = df[df.index.year == SAMPLED_YEAR]
#df_2018["PAR_15min"] = df_2018["surface_downwelling_photosynthetic_photon_flux_in_air_cm_time__sum_over_pt15m"]
#PAR_series = df_2018["PAR_15min"]#currently every 15 mins
#print(PAR_series)
#daily_avg = PAR_series.resample("D").mean().interpolate(method = "time")
daily_avg = df.to_frame()

daily_avg.to_parquet("Popof input data/PAR_popof.parquet")
plt.scatter(df.index, df)
plt.show()
