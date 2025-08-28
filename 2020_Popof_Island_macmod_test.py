'''Second iteration of G-MACMODS for Popof AK for 2020.
Also, updating chlorophyll to the correct Popof Island.'''

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
    'start_year': 2019,
    'start_month': 11,
    'start_day': 1,
    'calc_steps':   365

}
input_dict = mag_species.Saccharina
input_dict.update(param_dict)
input_dict['mp_spp_seed'] = 7
params = mag0.build_run_params(
    input_dict
)


#estimated harvest yield/amount of growline
SST_2020 = pd.read_parquet("Popof input data/2020-2020 SST processed.parquet")
SST_2021 = pd.read_parquet("Popof input data/2021-2021 SST processed.parquet") #this is missing data after September, but that may be fine since no growing post September anyways, its interpolated for Sept-Decprint(SST_df)
# last_day = SST_df.index[-1]
# new_last_day = SST_df.index[-1] + pd.DateOffset(days = 1)
# SST_df.loc[new_last_day] = SST_df.loc[last_day]
#SST_2020["sea_surface_temp"] = SST_2020["SST"]

two_years_SST = pd.concat([SST_2020, SST_2021])#.drop(columns = ["sea_surface_temp"]) #ignore_index=True
#two_years_SST = two_years_SST.resample("D").interpolate()
#two_years_SST.index = pd.date_range(start = "2020-01-01 00:00:00", end = "2021-12-31 00:00:00", freq = "D")
print(two_years_SST.columns)
plt.plot(two_years_SST.index, two_years_SST["WTMP"])
plt.xlabel("dates")
plt.ylabel("degrees C")
plt.title("SST data")
plt.savefig("../Kodiak files/Plots/2020_SST_Popof_Plot.png")
plt.show()
print(two_years_SST)
print(two_years_SST.shape)



SWH_df = pd.read_parquet("Popof input data/new_SWH_popof.parquet")
SWH_df.index = pd.date_range(start = "2020-01-01 00:00:00", periods = len(SWH_df), freq = "D")
last_day = SWH_df.index[-1]
new_last_day = SWH_df.index[-1] + pd.DateOffset(days = 1)
SWH_df.loc[new_last_day] = SWH_df.loc[last_day]
SWH = SWH_df["WVHT"]
SWH = SWH.values
SWH = pd.DataFrame(SWH)
two_years_SWH = pd.concat([SWH, SWH], ignore_index=True)
two_years_SWH_index = pd.date_range(start = "2019-01-01 00:00:00", end = "2021-01-01 00:00:00", freq = "D")
plt.plot(two_years_SWH_index, two_years_SWH)
plt.xlabel("dates")
plt.ylabel("meters")
plt.title("SWH data")
plt.show()
#SWH = .85 #in meters, this is from our data in prj_AM_UAF (link in comment at top)

MWP_df = pd.read_parquet("Popof input data/new_MWP_popof.parquet")
MWP_df.index = pd.date_range(start = "2020-01-01 00:00:00", periods = len(MWP_df), freq = "D")
last_day = MWP_df.index[-1]
new_last_day = MWP_df.index[-1] + pd.DateOffset(days = 1)
MWP_df.loc[new_last_day] = MWP_df.loc[last_day]
MWP = MWP_df["Peak Period"]
MWP = MWP.values
MWP = pd.DataFrame(MWP)
two_years_MWP = pd.concat([MWP, MWP], ignore_index=True)
two_years_MWP_index = pd.date_range(start = "2019-01-01 00:00:00", end = "2021-01-01 00:00:00", freq = "D")
plt.plot(two_years_MWP_index, two_years_MWP)
plt.xlabel("dates")
plt.ylabel("seconds")
plt.title("MWP data")
plt.show()
#MWP = 2.87 #no unit given but I assume s^-1, this is from our data in prj_AM_UAF (link in comment at top)

chlorophyll_df = pd.read_parquet("Popof input data/chl_popof.parquet")#using coordinates: lat=57.7, lon=-152
chl = chlorophyll_df["chl_conc"]
chl_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31", freq = "D")
chl = chl.loc[chl_2020].values
chl = pd.DataFrame(chl)
two_years_chl = pd.concat([chl, chl], ignore_index=True)
two_years_chl_index = pd.date_range(start = "2019-01-01 00:00:00", end = "2021-01-01 00:00:00", freq = "D")
plt.plot(two_years_chl_index, two_years_chl)
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
PAR = pd.DataFrame(PAR)
two_years_PAR = pd.concat([PAR, PAR], ignore_index=True)
two_years_PAR_index = pd.date_range(start = "2019-01-01 00:00:00", end = "2021-01-01 00:00:00", freq = "D")
plt.plot(two_years_PAR_index, two_years_PAR)
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
NO3 = pd.DataFrame(NO3)
two_years_NO3 = pd.concat([NO3, NO3], ignore_index=True)
two_years_NO3_index = pd.date_range(start = "2019-01-01 00:00:00", end = "2021-01-01 00:00:00", freq = "D")
plt.plot(two_years_NO3_index, two_years_NO3)
plt.xlabel("dates")
plt.ylabel("average uM nitrate (from 2, 5, and 10 m")
plt.title("Nitrate data")
plt.savefig("../Kodiak files/Plots/NO3_Popof_Plot.png")
plt.show()




input_data = two_years_SST, two_years_SWH, two_years_MWP, two_years_chl, two_years_PAR, two_years_NO3 #[SST_df["sea_surface_temp"], SWH_df["wave_height"], MWP_df["average_wpd_seconds"], chlorophyll_df["chl_conc"], PAR_df["PAR_15min"], NO3_df["Nox"]]
# for item in input_data:
#     print(item.head())
#     plt.plot(item.index, item, label = item.name)
# plt.legend()
# plt.show()
# plt.savefig("all_data.png")
forcing_index = pd.date_range(start="2019-01-01 00:00:00", end="2021-01-01 00:00:00", freq="D")
forcing = pd.DataFrame(
    {
        # Sea surface temperature (deg C)
        "sst":  two_years_SST.values.squeeze(),
        # Amount of light at the water surface. Not sure about the unit here,
        # it's probably something like mols/day or umol/s. I (Greta) think it
        #is either Einstein m-2 s-1 or daily avg because they got it from MODIS https://modis.gsfc.nasa.gov/data/dataprod/ipar.php
        "par":  two_years_PAR.values.squeeze(),
        # Chlorophyll, I think this contributed to turbidity?
        "chl":  two_years_chl.values.squeeze(),
        # Significant wave height, large wav
        "swh":  two_years_SWH.values.squeeze(),
        # Mean wave period, matters for nitrogen absorption (s)
        "mwp": two_years_MWP.values.squeeze(),
        # Pretty sure this is the ambient current, affects nitrogen uptake.
        # I think this is in m/s
        #"cmag": cmag_df["Speed (knots)"].iloc[[0, -1]],
        "cmag": .025 * len(forcing_index), #.025 is from eyeballing the Popof Island slides, refine later
        # Nitrate concentration. I think it's in concentration (mol/L)
        "no3": two_years_NO3.values.squeeze(),
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
print(forcing.head())
# %%
#
# for multiplier in [0.5, 1, 1.5]:
#     new_forcing = forcing.copy()
#     new_forcing["no3"] *= multiplier
#
#     growth_model = mag0.MAG0(params, new_forcing)
#     results = growth_model.compute()
#     print(results.head())
#
#     plt.plot(results.index, results.B / 1e3) #kg per m^2
# results
growth_model = mag0.MAG0(params, forcing)
results = growth_model.compute()

line3_df = pd.read_csv("../Kodiak files/env. inputs/lines/5-13-23.csv")
line3_df["Date"] = pd.to_datetime(line3_df["Date"])
line3_df.set_index(keys = "Date", inplace = True)
value3 = line3_df["Value"]

line6_df = pd.read_csv("../Kodiak files/env. inputs/lines/6-4-23.csv")
line6_df["Date"] = pd.to_datetime(line6_df["Date"])
line6_df.set_index(keys = "Date", inplace = True)
value6 = line6_df["Value"]

line7_df = pd.read_csv("../Kodiak files/env. inputs/lines/6-20-23.csv")
line7_df["Date"] = pd.to_datetime(line7_df["Date"])
line7_df.set_index(keys = "Date", inplace = True)
value7 = line7_df["Value"]

line4_df = pd.read_csv("../Kodiak files/env. inputs/lines/6-27-23.csv")
line4_df["Date"] = pd.to_datetime(line4_df["Date"])
line4_df.set_index(keys = "Date", inplace = True)
value4 = line4_df["Value"]

line8_df = pd.read_csv("../Kodiak files/env. inputs/lines/7-17-23.csv")
line8_df["Date"] = pd.to_datetime(line8_df["Date"])
line8_df.set_index(keys = "Date", inplace = True)
value8 = line8_df["Value"]

line5_df = pd.read_csv("../Kodiak files/env. inputs/lines/7-25-23.csv")
line5_df["Date"] = pd.to_datetime(line5_df["Date"])
line5_df.set_index(keys = "Date", inplace = True)
value5 = line5_df["Value"]

line9_df = pd.read_csv("../Kodiak files/env. inputs/lines/8-11-23.csv")
line9_df["Date"] = pd.to_datetime(line9_df["Date"])
line9_df.set_index(keys = "Date", inplace = True)
value9 = line9_df["Value"]

farm_size = 6800 #m^2 from "between spar buoys"
farm_grow_line = 6706 #m from "amount of grow-line"
biomass_kg_m2 = results.B / 1e3 #converts to kg/m^2
biomass_kg_m = biomass_kg_m2 * farm_size / farm_grow_line #converts to kg/m
plt.plot(results.index, biomass_kg_m, color = "blue")
plt.plot(line3_df.index, value3, color = "red")
plt.plot(line4_df.index, value4, color = "red")
plt.plot(line5_df.index, value5, color = "red")
plt.plot(line6_df.index, value6, color = "red")
plt.plot(line7_df.index, value7, color = "red")
plt.plot(line8_df.index, value8, color = "red")
plt.plot(line9_df.index, value9, color = "red")
plt.grid()
plt.xlabel("time")
plt.ylabel("kg of biomass/ m")
plt.title("Biomass estimates Popof Island, AK, 2020")
#plt.yscale("log")
plt.savefig("../Kodiak files/Plots/G-MACMOD_Popof_Plot.png")
fig,axes = plt.subplots(3,2,sharex = True)
env_names = ["sst", "par", "chl", "swh", "mwp", "no3"]
axes = axes.flatten()
for ax,name in zip(axes,env_names):
    ax.plot(results.index, forcing.loc[results.index,name])
    ax.set_title(name)
plt.show()
# sns.lineplot(results.reset_index(), x="date", y="B")
# sns.lineplot(results.reset_index(), x="date", y="d_Bm")
df = pd.DataFrame({"date": results.index, "biomass": biomass_kg_m * 1e3})
df.to_csv("GMACMODS_output.csv", index = False)
print("Done")
# %%

from magpy.mag_util import generate_standard_runs,postprocess,get_mask,eez_mask,csv_from_pp,get_area

# %%