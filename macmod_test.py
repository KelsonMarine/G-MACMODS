'''OLD VERSION. INSTEAD USE 2021_only_changed_sst_from_2020_macmod_test.py'''

from magpy import mag0
from magpy import mag_species
from multiprocessing import Pool
import numpy as np
import pandas as pd
# %%
from matplotlib import pyplot as plt
import seaborn as sns


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
    'calc_steps':   200
}
input_dict = mag_species.Saccharina
input_dict.update(param_dict)

params = mag0.build_run_params(
    input_dict
)

#metadata: chlorophyll: 2020-21 from NW Gulf of AK
#SST: 2017 offshore between Yakutat and Katalla
#NO3-2020 midwestern side of the Gulf of Alaska
#PAR-2020 glacier bay
#SWH-2009 near Montague Island
#CMAG- currently using eyeballed number from Popof Island from our slides
#everything else is left as it was before I (Greta) edited the code

cmag_df = pd.read_parquet("input data/cmag.parquet") #in m/s even though its labeled as knots. Only two months of data so I didn't end up using it


SST_df = pd.read_parquet("input data/SST.parquet")
SST = SST_df["sea_surface_temperature"]
SST = SST.resample("D").interpolate()
SST_2017 = pd.date_range(start = "2017-01-01 00:00:00", end = "2017-12-31 00:00:00", freq = "MS", tz = "UTC")
SST = SST.loc[SST_2017].values

SWH_df = pd.read_parquet("input data/SWH.parquet")#this data is a bit suspicious, but I sampled from an area that seemed reasonable (but it's only from apr-dec)
SWH = SWH_df["WVHT"]
SWH  = SWH.resample("D").interpolate()
SWH_2009 = pd.date_range(start = "2009-01-01 00:00:00", end = "2009-12-31 00:00:00", freq = "MS")
SWH = SWH.loc[SWH_2009].values

MWP_df = pd.read_parquet("input data/MWP.parquet")
MWP = MWP_df["sea_surface_wave_mean_period"]
MWP = MWP.resample("D").interpolate()
MWP_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00", freq = "MS", tz = "UTC")
MWP = MWP.loc[MWP_2020].values

chlorophyll_df = pd.read_parquet("input data/chlorophyll.parquet")
chl = chlorophyll_df["mass_concentration_of_chlorophyll_in_sea_water"]
chl = chl.resample("D").interpolate()
chl_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31", freq = "MS", tz = "UTC")
chl = chl.loc[chl_2020].values

PAR_df = pd.read_parquet("input data/PAR.parquet")
PAR = PAR_df["par"]
PAR = PAR.resample("D").interpolate()
PAR_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00",freq = "MS")
print(PAR_2020)
PAR = PAR.loc[PAR_2020].values

NO3_df = pd.read_parquet("input data/NO3.parquet")
NO3 = NO3_df["NO3 concentration"]
NO3 = NO3.resample("D").interpolate()
NO3_2020 = pd.date_range(start = "2020-01-01 00:00:00", end = "2020-12-31 00:00:00",freq = "MS")
NO3 = NO3.loc[NO3_2020].values
input_data = [cmag_df["Speed (m/s)"], SST_df["sea_surface_temperature"], SWH_df["WVHT"], MWP_df["sea_surface_wave_mean_period"], chlorophyll_df["mass_concentration_of_chlorophyll_in_sea_water_qc_agg"], PAR_df["par"], NO3_df["NO3 concentration"]]
for item in input_data:
    print(item.head())
    plt.plot(item.index, item, label = item.name)
plt.legend()
plt.show()
forcing_index = pd.date_range(start="2020-01-01 00:00:00", end="2020-12-31 00:00:00", freq="MS")
forcing = pd.DataFrame(
    {
        # Sea surface temperature (deg C)
        "sst": SST,
        # Amount of light at the water surface. Not sure about the unit here,
        # it's probably something like mols/day or umol/s
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
        "cmag": .03 * len(forcing_index), #.02 is from eyeballing the Popof Island slides, refine later
        # Environmental nitrogen, not sure about the unit or what exactly is
        # being measured here. I think it's in concentration (mol/L)
        "no3": NO3,
        #I think this is nitrogen flux but it may be nutrient flux
        "nflux": [0] * len(forcing_index),
        "seed": [1] * len(forcing_index),
        # Latitude, matters for daylight duration
        "ylat": [43] * len(forcing_index),
        # This doesn't do anything in this single point case
        "xlon360": [250] * len(forcing_index),
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

    plt.plot(results.index, results.B / 1e3)
results





plt.plot(results.index, results.B / 1e3)
plt.show()
# sns.lineplot(results.reset_index(), x="date", y="B")
# sns.lineplot(results.reset_index(), x="date", y="d_Bm")

# %%

from magpy.mag_util import generate_standard_runs,postprocess,get_mask,eez_mask,csv_from_pp,get_area

# %%