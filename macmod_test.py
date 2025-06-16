


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
}
input_dict = mag_species.Saccharina
input_dict.update(param_dict)

params = mag0.build_run_params(
    input_dict
)
forcing = pd.DataFrame(
    {
        # Sea surface temperature (deg C)
        "sst": [10, 10],
        # Amount of light at the water surface. Not sure about the unit here,
        # it's probably something like mols/day or umol/s
        "par": [20, 20],
        # Chlorophyll, I think this contributed to turbidity?
        "chl": [0, 0],
        # Significant wave height, large wav
        "swh": [0, 0],
        # Mean wave period, matters for nitrogen absorption (s)
        "mwp": [4, 4],
        # Pretty sure this is the ambient current, affects nitrogen uptake.
        # I think this is in m/s
        "cmag": [0.3, 0.3],
        # Environmental nitrogen, not sure about the unit or what exactly is
        # being measured here.
        "no3": [0.5, 0.5],
        "nflux": [0, 0],
        "seed": [1, 1],
        # Latitude, matters for daylight duration
        "ylat": [43, 43],
        # This doesn't do anything in this single point case
        "xlon360": [250, 250],
        "var": [0.1] * 2
    },
    index=pd.DatetimeIndex(["1/1/2003 00:00:00", "1/1/2004 00:00:00"]),
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