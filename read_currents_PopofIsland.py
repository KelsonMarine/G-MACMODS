'''https://tds.hycom.org/thredds/catalogs/GLBu0.08/reanalysis.html?dataset=GLBu0.08-reanalysis with OPENDAP
uses coordinates (55.38,-160.95) near Popof Island'''

import xarray as xr
import pandas as pd

url = 'https://tds.hycom.org/thredds/dodsC/GLBu0.08/reanalysis'

ds = xr.open_dataset(url, decode_times=False)
ds = ds.sel(lat = 55.38, lon = -160.95, method = "nearest").squeeze()
ds = ds.sel(time = slice(96432, 105192))
ds_20m = ds.sel(depth = ds.depth.where(ds.depth <= 20, drop = True))
print(ds_20m)
print(ds_20m["water_u"].values)
print(ds_20m["water_v"].values)
eastward_20m = ds_20m["water_u"].mean(dim = "depth")
northward_20m = ds_20m["water_v"].mean(dim = "depth")
combined_df = xr.Dataset({"eastward_velocity": eastward_20m, "northward_velocity": northward_20m})
df = combined_df.to_dataframe().reset_index()
df.to_csv("../Kodiak files/env. inputs/overall_velocity_PopofIsland.csv")
file = pd.read_csv("../Kodiak files/env. inputs/overall_velocity_PopofIsland.csv")
file["velocity"] = (file[""])


#
#
# import xarray as xr
# import pandas as pd
#
# url = 'https://tds.hycom.org/thredds/dodsC/GLBu0.08/reanalysis'
#
# ds = xr.open_dataset(url, decode_times=False)
# ds = ds.sel(lat = 57.801058, lon = -152.327786, method = "nearest").squeeze()
# ds = ds.sel(time = slice(96432, 105192))
# ds_20m = ds.sel(depth = ds.depth.where(ds.depth <= 20, drop = True))
# eastward_20m = ds_20m["water_u"].mean(dim = "depth")
# northward_20m = ds_20m["water_v"].mean(dim = "depth")
# eastward_df = eastward_20m.to_dataframe().reset_index()
# northward_df = northward_20m.to_dataframe().reset_index()
# eastward_df.to_csv("../Kodiak files/env. inputs/eastward_velocity1.csv", index = False)
# northward_df.to_csv("../Kodiak files/env. inputs/northward_velocity1.csv", index = False)
# print("DONE")


# selected_cols = ds[["time", "water_u", "water_v"]]
# print(ds)
# df = selected_cols.to_dataframe()
# df.to_csv("../Kodiak files/env. inputs/velocity_data1.csv")
# print("DONE")