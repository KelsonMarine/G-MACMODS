'''
THIS WAS USED FOR CHLOROPHYLL IN 2020_Popof_Island_macmod_test.py, I turned the list in this into a csv file and then put that into read_chl_Popof_USETHIS.py
Code created 7/18/25
daily chlorophyll data at coordinates (57.7, -152) near Popof Island, daily data
data source: https://portal.aoos.org/#module-metadata/5d7b00c1-73c7-4861-af87-a7857c358d02/4779f835-7bd3-4f92-841a-e419c4e9e2c3
mass in units of ug kg-1'''
from siphon.catalog import TDSCatalog
import xarray
import numpy as np
import os

catalog_url = "https://thredds.aoos.org/thredds/catalog/aoos/gak_bgc_v2/nicecubes/catalog.xml"
catalog = TDSCatalog(catalog_url)
cat_2020 = catalog.catalog_refs["2020"].follow()
list_of_average_chl = []
counter = 0
for data in list(cat_2020.datasets)[0:]: #replace 0 with whatever data point you want to start on
    dataset = cat_2020.datasets[data]
    print(dataset.access_urls)
    filename = f"{data}.nc"
    ds = dataset.download(filename)
    counter += 1
    xr_data = xarray.load_dataset(filename)
    popof_chlor = xr_data["mass_concentration_of_chlorophyll_a_in_sea_water"].sel(lat=57.7, lon=-152, method="nearest")
    top_layer_vals = popof_chlor.values[0, :4]
    avg_top_layer = np.nanmean(top_layer_vals)
    list_of_average_chl.append(avg_top_layer)
    print(list_of_average_chl)
    os.remove(filename)

