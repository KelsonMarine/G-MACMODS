# from netCDF4 import Dataset
# file_path = '../Kodiak files/temperate_brown_nitrate_limited_group1.nc'
# dataset = Dataset(file_path, 'r')
# print(dataset)
# import xarray as xr
# ds = xr.open_dataset("../Kodiak files/temperate_brown_ambient_nitrate_Copernicus.nc")
# df = ds.to_dataframe()
# df.to_csv("../Kodiak files/temperate_brown_ambient_nitrate_Copernicus.csv")
from scipy.io import loadmat
mat_data = loadmat("../Kodiak files/waves_currents.mat")
print(mat_data.keys())
