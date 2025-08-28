#
# import xarray as xr
# import pandas as pd
#
# url = "https://coastwatch.noaa.gov/erddap/griddap/noaacwNPPVIIRSSQchlaDaily.nc?chlor_a%5B(2012-01-03T12:00:00Z):1:(2025-05-22T12:00:00Z)%5D%5B(0.0):1:(0.0)%5D%5B(89.75625):1:(-89.75625)%5D%5B(-179.98125):1:(179.98125)%5D"
# ds = xr.open_dataset(url, decode_times=False)
# ds = ds.sel(lat = 55.386045, lon = -160.425742, method = "nearest").squeeze()
# print(ds)
#https://portal.edirepository.org/nis/mapbrowse?packageid=edi.1756.1 seemed good but each file is many many MB
'''https://portal.aoos.org/#platform/c5fbd846-efc1-5e82-8ea0-25bb36b20929/v2?c=rainbow&pid=187
I didn't end up using this for the input, see read_newchlorophyll.py'''
import pandas as pd
df = pd.read_csv("../Kodiak files/env. inputs/chlorophyll.csv")
print(df.columns)
print(df["chlorophylla"])
not_NaN = df["chlorophylla"].count()
print(not_NaN)