

from magpy import mag0
from magpy import mag_species
from multiprocessing import Pool
import numpy as np
import pandas as pd
# %%
from matplotlib import pyplot as plt
import seaborn as sns

from read_SST_PopofIsland import SST_daily_2020

param_dict = {
    "output_path": "./output",
    # I don't know what these _feq params are,
    # but they're definition is important to avoid errors.
    # These are set as 8 in mag_std_runs_paper.py
    "Growth2_freq": 8,
    "d_Be_freq": 8,
    "d_Bm_freq": 8,
    "d_Ns_freq": 8,
    "harv_freq": 8,
    "GRate_freq": 8,
    "B_N_freq": 8,
    "n_harv_freq": 8,
    "min_lim_freq": 8,
    "gQ_freq": 8,
    "gT_freq": 8,
    "gE_freq": 8,
    "gH_freq": 8,
    # -1 Turns off harvesting
    "mp_harvest_schedule": -1,
    # 0 means to not limit the nitrogen just to possible upwelling
    "mp_N_flux_limit": 0,
    # The deathrate (day^-1), this has a significant effect on the results
    "mp_spp_death": 0.01,
    # Line separation, with high enough yields and small enough spacings you
    # can get crowding effects
    "mp_spp_line_sep": 5.0,
    'start_year': 2020,
    'start_month': 1,
    'start_day': 1,
    'calc_steps':   365
}
input_dict = mag_species.Saccharina
input_dict.update(param_dict)

params = mag0.build_run_params(
    input_dict
)

SST_df = pd.read_parquet("Popof input data/SST_popof.parquet") #this is missing data after Dec 12 (but I added one point on 12/31)
SST = SST_df["sea_surface_temp"]
SST_df.loc[pd.Timestamp("2020-12-31")] = 5.429167#this is just the first value from January, we assume its cyclical
SST_df = SST_df.sort_index()
SST = SST_df["sea_surface_temp"].resample("D").interpolate()
SST_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00", freq = "D")
SST = SST.loc[SST_2020].values
plt.plot(SST_2020, SST)
plt.xlabel("dates")
plt.ylabel("degrees C")
plt.title("SST data")
plt.savefig("../Kodiak files/Plots/SST_Popof_Plot.png")
plt.show()



SWH_df = pd.read_parquet("Popof input data/WVHT_popof.parquet")
# SWH = SWH_df["wave_height"]
SWH_df.loc[pd.Timestamp("2020-12-31"), "wave_height"] = 4.444583 #this is just the first value from January, we assume its cyclical
SWH_df = SWH_df.sort_index()
SWH = SWH_df["wave_height"].resample("D").interpolate()
SWH_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00", freq = "D")
SWH = SWH.reindex(SWH_2020).interpolate(limit_direction = "both")
SWH = SWH.values
plt.plot(SWH_2020, SWH)
plt.xlabel("dates")
plt.ylabel("meters")
plt.title("SWH data")
plt.savefig("../Kodiak files/Plots/SWH_Popof_Plot.png")
plt.show()

MWP_df = pd.read_parquet("Popof input data/MWP_popof.parquet")
MWP = MWP_df["average_wpd_seconds"]
MWP = MWP.resample("D").interpolate()
MWP_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00", freq = "D")
MWP = MWP.loc[MWP_2020].values
plt.plot(MWP_2020, MWP)
plt.xlabel("dates")
plt.ylabel("seconds (converted from nanoseconds)")
plt.title("MWP data")
plt.savefig("../Kodiak files/Plots/MWP_Popof_Plot.png")
plt.show()

chlorophyll_df = pd.read_parquet("Popof input data/chl_popof.parquet")
chl = chlorophyll_df["chl_conc"]
chl_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31", freq = "D")
chl = chl.loc[chl_2020].values
plt.plot(chl_2020, chl)
plt.xlabel("dates")
plt.ylabel("ug/kg")
plt.title("Chlorophyll data")
plt.savefig("../Kodiak files/Plots/chl_Popof_Plot.png")
plt.show()

PAR_df = pd.read_parquet("Popof input data/PAR_popof.parquet")
PAR_df.index = pd.date_range(start = "2020-01-01 00:00:00", periods = len(PAR_df), freq = "D")
last_day = PAR_df.index[-1]
new_last_day = PAR_df.index[-1] +pd.DateOffset(days = 1)
PAR_df.loc[new_last_day] = PAR_df.loc[last_day]
PAR = PAR_df["PAR_15min"]
PAR = PAR.values
plt.plot(PAR_df.index, PAR)
plt.xlabel("dates")
plt.ylabel("mmol photons/m^2")
plt.title("Photosynthetically Active Radiation data")
plt.savefig("../Kodiak files/Plots/PAR_Popof_Plot.png")
plt.show()


NO3_df = pd.read_parquet("Popof input data/NO3_popof.parquet")
NO3 = NO3_df["Nox"]
NO3 = NO3.resample("D").interpolate() #this data is quite spotty so this will probably create some questionable data but we only got some data points from Michael Stekoll
NO3_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00", freq = "D")
NO3 = NO3.loc[NO3_2020].values
plt.plot(NO3_2020, NO3)
plt.xlabel("dates")
plt.ylabel("average uM nitrate (from 2, 5, and 10 m")
plt.title("Nitrate data")
plt.savefig("../Kodiak files/Plots/NO3_Popof_Plot.png")
plt.show()



print(len(SST_df["sea_surface_temp"]))
print(len(SWH_df["wave_height"]))
print(len(MWP_df["average_wpd_seconds"]))
print(len(chlorophyll_df["chl_conc"]))
print(len(PAR_df["PAR_15min"]))
print(len(NO3))



input_data = SST, SWH, MWP, chl, PAR, NO3 #[SST_df["sea_surface_temp"], SWH_df["wave_height"], MWP_df["average_wpd_seconds"], chlorophyll_df["chl_conc"], PAR_df["PAR_15min"], NO3_df["Nox"]]
# for item in input_data:
#     print(item.head())
#     plt.plot(item.index, item, label = item.name)
# plt.legend()
# plt.show()
# plt.savefig("all_data.png")
forcing_index = pd.date_range(start="2020-01-01 00:00:00", end="2020-12-31 00:00:00", freq="D")
forcing = pd.DataFrame(
    {
        # Sea surface temperature (deg C)
        "sst": SST,
        # Amount of light at the water surface. Not sure about the unit here,
        # it's probably something like mols/day or umol/s. I (Greta) think it
        #is either Einstein m-2 s-1 or daily avg because they got it from MODIS https://modis.gsfc.nasa.gov/data/dataprod/ipar.php
        "par": PAR,
        # Chlorophyll, I think this contributed to turbidity?
        "chl": chl,
        # Significant wave height, large wav
        "swh": SWH,
        # Mean wave period, matters for nitrogen absorption (s)
        "mwp": MWP,
        # Pretty sure this is the ambient current, affects nitrogen uptake.
        # I think this is in m/s
        #"cmag": cmag_df["Speed (knots)"].iloc[[0, -1]],
        "cmag": .025 * len(forcing_index), #.025 is from eyeballing the Popof Island slides, refine later
        # Nitrate concentration. I think it's in concentration (mol/L)
        "no3": NO3,
        #I think this is nitrogen flux but it may be nutrient flux
        "nflux": [0] * len(forcing_index),
        "seed": [1] * len(forcing_index),
        # Latitude, matters for daylight duration
        "ylat": [57.7] * len(forcing_index),
        # This doesn't do anything in this single point case
        "xlon360": [-152.4] * len(forcing_index),#or this may have to be out of 360, not the normal lon convention, change if error
        "var": [0.1] * len(forcing_index)
    },
    index=forcing_index #points in time
)
print(forcing.shape)

# %%
for multiplier in [0.5, 1.0, 1.5]:
    new_forcing = forcing.copy()
    new_forcing["no3"] *= multiplier

    growth_model = mag0.MAG0(params, new_forcing)
    results = growth_model.compute()

    plt.plot(results.index, results.B / 1e3) #kg per m^2
results



plt.plot(results.index, results.B / 1e3)
plt.xlabel("time")
plt.ylabel("kg of biomass/ m^2")
plt.title("Biomass estimates Popof Island, AK")
plt.savefig("../Kodiak files/Plots/G-MACMOD_Popof_Plot.png")
plt.show()
# sns.lineplot(results.reset_index(), x="date", y="B")
# sns.lineplot(results.reset_index(), x="date", y="d_Bm")

# %%

from magpy.mag_util import generate_standard_runs,postprocess,get_mask,eez_mask,csv_from_pp,get_area

# %%