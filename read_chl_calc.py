'''This is the original draft, but it has the incorrect location, see read_newchlorophyll.py for the correct data'''

import xarray
import numpy as np
from siphon.catalog import TDSCatalog
import os
#
# catalog_url = "https://thredds.aoos.org/thredds/catalog/aoos/gak_bgc_v2/nicecubes/catalog.xml"
# catalog = TDSCatalog(catalog_url)
# cat_2020 = catalog.catalog_refs["2020"].follow()
# dataset = cat_2020.datasets[2]
# print(dataset)
# ds = xarray.load_dataset("avg_2019-01-01-00.nc")
# popof_chlor = ds["mass_concentration_of_chlorophyll_a_in_sea_water"].sel(lat=55.4, lon=-160.5, method="nearest")
# print(popof_chlor)
# print(ds.data_vars.keys())
#
# print(ds["mass_concentration_of_chlorophyll_a_in_sea_water"])
# popof_chlor = ds["mass_concentration_of_chlorophyll_a_in_sea_water"].sel(lat = 55.4, lon = -160.5, method = "nearest") #selecting near popof island for data\
# top_layer_vals = popof_chlor.values[0,:4]
# avg_top_layer = np.nanmean(top_layer_vals)
#print(avg_top_layer)


catalog_url = "https://thredds.aoos.org/thredds/catalog/aoos/gak_bgc_v2/nicecubes/catalog.xml"
catalog = TDSCatalog(catalog_url)
#print(list(catalog.catalog_refs))
#print(list(catalog.datasets))
cat_2020 = catalog.catalog_refs["2020"].follow()
list_of_average_chl = []
counter = 0
for data in list(cat_2020.datasets):
    dataset = cat_2020.datasets[data]
    print(dataset.access_urls)
    filename = f"{data}.nc"
    ds = dataset.download(filename)#if you pass a filename, it'll save it to that
    counter += 1
    xr_data = xarray.load_dataset(filename)
    popof_chlor = xr_data["par"].sel(lat=55.4, lon=-160.5, method="nearest")  # selecting near incorrect popof island for data
    top_layer_vals = popof_chlor.values[0, :4]
    print(top_layer_vals)
    avg_top_layer = np.nanmean(top_layer_vals)
    list_of_average_chl.append(avg_top_layer)
    #xr_data[""]
    #print(ds)
    print(list_of_average_chl)
    os.remove(filename)
    exit()
