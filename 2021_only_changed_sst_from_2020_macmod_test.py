'''Third iteration of G-MACMODS for Popof AK for 2020. This version works better with dates/leap years and is less date-sensitive.
Chlorophyll has correct coordinates (previously was an issue). The name of this file is actually wrong,  SST, PAR, and NO3 all vary
between years (at least for 2019-20 and 2020-21) because there is the correct data for that, but chl, SWH, and MWP don't change between these years.'''


import numpy as np
import pandas as pd

from read_SST_NOAA_buoy_KDAA2_data import start_year
from utils import build_forcing, offset_data_year
from magpy import mag0, mag_species
from datetime import date
import pytz

# %%
from matplotlib import pyplot as plt

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

MAKE_PLOTS = False
#SST input file order:
#for all SST, data is coming from this website: https://www.ndbc.noaa.gov/station_page.php?station=kdaa2
#SST_2019: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2019_2019.parquet -> read_SST_2019_Popof_USEME.py -> Popof input data/2019-2019 SST processed.parquet
#SST_2020: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2020_2020.parquet -> read_SST_2020_Popof_USEME.py -> Popof input data/2020-2020 SST processed.parquet
#SST_2021: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2021_2021.parquet -> read_SST_2021_Popof_USEME.py -> Popof input data/2021-2021 SST processed.parquet

#remember to only have 2019 and 2020 or 2020 and 2021 here, not all 3, and change two_years_SST accordingly
SST_2019 = pd.read_parquet("Popof input data/2019-2019 SST processed.parquet")
SST_2020 = pd.read_parquet("Popof input data/2020-2020 SST processed.parquet") #this is missing data after September, but that may be fine since no growing post September anyways, its interpolated for Sept-Decprint(SST_df)
SST_2021 = pd.read_parquet("Popof input data/2021-2021 SST processed.parquet")
all_years_SST = pd.concat([SST_2019, SST_2020, SST_2021])
two_years_SST = all_years_SST[all_years_SST.index.year.isin([start_year, start_year + 1])]#.drop(columns = ["sea_surface_temp"]) #ignore_index=True
if MAKE_PLOTS:
    plt.plot(two_years_SST.index, two_years_SST["WTMP"])
    plt.xlabel("dates")
    plt.ylabel("degrees C")
    plt.title("SST data")
    plt.savefig("../Kodiak files/Plots/2020_SST_Popof_Plot.png")
    plt.show()
print(two_years_SST.index.tz)

#SWH input data file order:
#https://maps.nrel.gov/marine-energy-atlas/data-viewer/download -> Kodiak_waves_new.csv -> read_SWH_Popof_new.py -> new_SWH_popof.parquet

SWH_df = pd.read_parquet("Popof input data/new_SWH_popof.parquet")
SWH = SWH_df["Significant Wave Height"]
if MAKE_PLOTS:
    plt.plot(SWH.index, SWH)
    plt.xlabel("dates")
    plt.ylabel("meters")
    plt.title("SWH data")
    plt.show()
print(SWH.index.tz)


#MWP input data file order:
#https://maps.nrel.gov/marine-energy-atlas/data-viewer/download -> Kodiak_waves_new.csv -> read_MWP_Popof_new.py -> new_MWP_popof.parquet

MWP_df = pd.read_parquet("Popof input data/new_MWP_popof.parquet")
MWP = MWP_df["Peak Period"]
if MAKE_PLOTS:
    plt.plot(MWP.index, MWP)
    plt.xlabel("dates")
    plt.ylabel("seconds")
    plt.title("MWP data")
    plt.show()
print(MWP.index.tz)

#chl input data files order:
#data link: https://portal.aoos.org/#module-metadata/5d7b00c1-73c7-4861-af87-a7857c358d02/4779f835-7bd3-4f92-841a-e419c4e9e2c3
#read_newchlorophyll.py ->creates a lst that I copied into a CSV file. The lst is also in read_chl_input_lst (if you want to see it), but I saved the file which was a CSV with two
#columns, Date and Value. this csv (chl_data_Popof.csv) goes into -> read_chl_Popof_USETHIS.py -> chl_popof.parquet

chlorophyll_df = pd.read_parquet("Popof input data/chl_popof.parquet")#using coordinates: lat=57.7, lon=-152
chl = chlorophyll_df["chl_conc"]
if MAKE_PLOTS:
    plt.plot(chl.index, chl)
    plt.xlabel("dates")
    plt.ylabel("ug/kg")
    plt.title("Chlorophyll data")
    plt.savefig("../Kodiak files/Plots/chl_Popof_Plot.png")
    plt.show()
print(chl.index.tz)

#PAR input data files order:
#https://portal.aoos.org/#metadata/75407/station/data -> PAR-anchor-point-AK.csv ->read_PAR_PopofIsland.py -> PAR_popof.parquet

PAR_df = pd.read_parquet("Popof input data/PAR_popof.parquet")
PAR = PAR_df["surface_downwelling_photosynthetic_photon_flux_in_air_cm_time__sum_over_pt15m"]
if MAKE_PLOTS:
    plt.plot(PAR.index, PAR)
    plt.xlabel("dates")
    plt.ylabel("mmol photons/m^2")
    plt.title("Photosynthetically Active Radiation data")
    plt.savefig("../Kodiak files/Plots/PAR_Popof_Plot.png")
    plt.show()
print(PAR.index.tz)

#NO3 input data files order:
#to get data, I used NOx graphs that were emailed from Michael Stekoll to Toby and me and used software that turns graphs into data points. I put the data points into CSV files.
#CSV files (Kodiak files/env. inputs/NOx INPUTS/) -> read_NO3_math_PopofIsland.py -> NO3_popof.parquet

NO3_df = pd.read_parquet("Popof input data/NO3_popof.parquet")#this data is quite spotty so this will probably create some questionable data but we only got some data points from Michael Stekoll
NO3 = NO3_df["Nox"]
if MAKE_PLOTS:
    plt.plot(NO3.index, NO3)
    plt.xlabel("dates")
    plt.ylabel("average uM nitrate (from 2, 5, and 10 m")
    plt.title("Nitrate data")
    plt.savefig("../Kodiak files/Plots/NO3_Popof_Plot.png")
    plt.show()
print(NO3.index.tz)


forcing_index = pd.date_range(start=date(input_dict["start_year"], input_dict["start_month"], input_dict["start_day"]), end="2022-01-01 00:00:00", freq="D")

# This provides the data that will be used for forcing the model
# The key of each entry is the column name in the final forcing dataframe
# The value for each entry is either a single number to repeat for the entire period, or a dataframe/series with a DatetimeIndex
# The data will be made to fit the given forcing index by interpolation and repeating the value for the nearest year with data
# So it effectively assumes the data is yearly cyclical and uses the closest provided year for the data.
# Then it re-interpolates the data to match the forcing index exactly. This will
# handle leap years when data was given for a non-leap year by interpolating
# February 28th and March 1st for the year with data.
forcing_data = {
    # Sea surface temperature (deg C)
    "sst":  two_years_SST,
    # Amount of light at the water surface. Not sure about the unit here,
    # it's probably something like mols/day or umol/s. I (Greta) think it
    #is either Einstein m-2 s-1 or daily avg because they got it from MODIS https://modis.gsfc.nasa.gov/data/dataprod/ipar.php
    "par":  offset_data_year(PAR, -1),
    # Chlorophyll, I think this contributed to turbidity?
    "chl":  chl,
    # Significant wave height, large wave
    "swh":  SWH,
    # Mean wave period, matters for nitrogen absorption (s)
    "mwp": MWP,
    # Pretty sure this is the ambient current, affects nitrogen uptake.
    # I think this is in m/s
    #"cmag": cmag_df["Speed (knots)"].iloc[[0, -1]],
    "cmag": .025, #.025 is from eyeballing the Popof Island slides in shared google drive, refine later
    # Nitrate concentration. I think it's in concentration (mol/L)
    "no3": NO3,
    #I think this is nitrogen flux but it may be nutrient flux
    "nflux": 0,
    "seed": 1,
    # Latitude, matters for daylight duration
    "ylat": 57.7,
    # This doesn't do anything in this single point case
    "xlon360": -152.4 #or this may have to be out of 360, not the normal lon convention, change if error
}
forcing = build_forcing(forcing_index, forcing_data)

print(forcing.shape)
print(forcing.head())
# %%
#
# for multiplier in [0.5, 1, 1.5]:
#     new_forcing = forcing.copy()
#     new_forcing["par"] *= multiplier
#     growth_model = mag0.MAG0(params, new_forcing)
#     results = growth_model.compute()
#     print(results.head())
#     plt.plot(results.index, results.B / 1e3, color = "orange") #kg per m^2

#SENSITIVITY ANALYSIS
new_forcing = forcing.copy()
new_forcing["mwp"] += 0
growth_model = mag0.MAG0(params, new_forcing)
results = growth_model.compute()
print(results.head())
plt.plot(results.index, results.B / 1e3, color = "green", label = "original", linewidth = 2) #kg per m^2 linewidth = 2.75,

new_forcing = forcing.copy()
new_forcing["mwp"] *= 1.2
growth_model = mag0.MAG0(params, new_forcing)
results = growth_model.compute()
print(results.head())
plt.plot(results.index, results.B / 1e3, color = "purple", label = "*1.2") #kg per m^2

new_forcing = forcing.copy()
new_forcing["mwp"] *= 1.5
growth_model = mag0.MAG0(params, new_forcing)
results = growth_model.compute()
print(results.head())
plt.plot(results.index, results.B / 1e3, color = "orange", label = "1.5x") #kg per m^2

# new_forcing = forcing.copy()
# new_forcing[""] *= 1.5
# growth_model = mag0.MAG0(params, new_forcing)
# results = growth_model.compute()
# print(results.head())
# plt.plot(results.index, results.B / 1e3, color = "pink", label = "1.4x") #kg per m^2
plt.legend()
plt.savefig("../../code/G-MACMODS sensitivity analysis/sst.png")
plt.show()
#results
growth_model = mag0.MAG0(params, forcing)
results = growth_model.compute()

#These lines are to compare where the Kodiak farm was at these points compared to where G-MACMODS predicts.
#I think something weird happened with their alignment, but they should be lined up with the graph (just edit the dates so they are)
#This section of line_x_df isn't necessary for running the model.

line3_df = pd.read_csv("../Kodiak files/env. inputs/lines/5-13-23.csv") #the lines I imported are just line sections I created at the correct heights.
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

#set these to the actual size of your farm, it will have an impact on the output
farm_size = 6800 #m^2 from "between spar buoys"
farm_grow_line = 6706 #m from "amount of grow-line"
biomass_kg_m2 = results.B / 1e3 #converts to kg/m^2
biomass_kg_m = biomass_kg_m2 * farm_size / farm_grow_line #converts to kg/m
plt.plot(results.index, biomass_kg_m, color = "blue")

#this plots are where the Stekoll growth was at these times (based off the graph of 2023 in the Stekoll paper)
# plt.plot(line3_df.index, value3, color = "red")
# plt.plot(line4_df.index, value4, color = "red")
# plt.plot(line5_df.index, value5, color = "red")
# plt.plot(line6_df.index, value6, color = "red")
# plt.plot(line7_df.index, value7, color = "red")
# plt.plot(line8_df.index, value8, color = "red")
# plt.plot(line9_df.index, value9, color = "red")

plt.grid()
plt.xlabel("time")
plt.ylabel("kg of biomass/ m")
plt.title("Biomass estimates Popof Island, AK, 0")
#plt.yscale("log")
#plt.savefig("../../code/model comparisons/2020/output with new SST data/GMACMODS_output_2019-2020.png")
fig,axes = plt.subplots(3,2,sharex = True)
fig.set_size_inches(12, 12)
env_names = ["sst", "par", "chl", "swh", "mwp", "no3"]

axes = axes.flatten()
for ax,name in zip(axes,env_names):
    ax.plot(results.index, forcing.loc[results.index,name])
    ax.set_title(name)
fig.savefig(f"../../code/model comparisons/forcing_plots_{start_year}-{start_year + 1}.png")
plt.show()

df = pd.DataFrame({"date": results.index, "biomass": biomass_kg_m * 1e3})
df.to_csv(f"../../code/model comparisons/{start_year + 1}/output with new SST data/GMACMODS_output_{start_year}-{start_year + 1}.csv", index = False)
print("Done")
# %%

from magpy.mag_util import generate_standard_runs,postprocess,get_mask,eez_mask,csv_from_pp,get_area

# %%