# G-MACMODS
Global MacroAlgae Cultivation MODeling System (G-MACMODS)
============================================================================
Isabella Arzeno-Soltero
Benjamin T. Saenz
Kristen Davis

Edited by Alex + Greta

Updated: 8/29/2025

This has the findings from Greta's work: https://docs.google.com/document/d/1G2zV2E-qxUsmNoKITmxFjuJ9bn5ecFEtDzwDUgAtY18/edit?usp=sharing

FILES ORGANIZATION:

The most recent version of the model is 2021_only_changed_sst_from_2020_macmod_test.py and this
is what should be used. Other models have outdated file inputs and may have date issues/old environmental
data inputs.

Files named read_{environmental parameter}.py or that with a number after it
are inputs to the initial run of macmods_test.py, and are to model Southeast AK 
more generally. These should not be used for the site in Kodiak, AK.

For the DEB model, read_DEB_input_DIC.py and files created by read_SST_NOAA_buoy_data.py
are used. I turned the df from read_SST_NOAA_buoy_data.py into a CSV which I then used. The
other parameters use files that were downloaded from the original source.

All other files are for Popof Island, close to Kodiak, AK or for model validation/comparison
runs. These files should have their source and location (but if the filename has Popof
in it, and it doesn't say the location, it is near Popof). I put the path from the download
location to the parquet version that is fed into the model next to the read in parquet section
of code for each environmental dataset. Data was put into parquet format
and then into 2020_Popof_Island_macmod_test.py or the 2021 versions. 

A lot of the data only had one year of high quality data, so that year was selected and then dates were edited
to align the dates over one year. The only difference between the 2020 and 2021 versions 
in terms of environmental data is the year that SST data was selected for. The difference
between the 2021_Popof_Island_macmod_test.py and 2021_only_changed_sst_from_2020_macmod_test.py
is that Alex developed some functions that better process dates and lead to fewer issues
when dealing with things such as leap years, which is especially important when using data
from different years. These were implemented in the 2021_only_changed....py.

File organization: the files for input data for G-MACMODS are in the Kodiak files folder, all files for the
DEB model are in the DEB model folder

G-MACMODS:if you put in the start_year, the inputs should be for the year that they have data closest to that,
if they have multiple years. You can also offset the data year in the forcing_data dictionary.

DATA USED FOR G-MACMODS:
SST: https://www.ndbc.noaa.gov/station_page.php?station=kdaa2
SST_2019: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2019_2019.parquet -> read_SST_2019_Popof_USEME.py -> Popof input data/2019-2019 SST processed.parquet
SST_2020: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2020_2020.parquet -> read_SST_2020_Popof_USEME.py -> Popof input data/2020-2020 SST processed.parquet
SST_2021: read_SST_NOAA_buoy_KDAA2_data.py -> Popof input data/kdaa2_2021_2021.parquet -> read_SST_2021_Popof_USEME.py -> Popof input data/2021-2021 SST processed.parquet
SWH: https://maps.nrel.gov/marine-energy-atlas/data-viewer/download -> Kodiak_waves_new.csv -> read_SWH_Popof_new.py -> new_SWH_popof.parquet
MWP: https://maps.nrel.gov/marine-energy-atlas/data-viewer/download -> Kodiak_waves_new.csv -> read_MWP_Popof_new.py -> new_MWP_popof.parquet
chl: https://portal.aoos.org/#module-metadata/5d7b00c1-73c7-4861-af87-a7857c358d02/4779f835-7bd3-4f92-841a-e419c4e9e2c3
read_newchlorophyll.py ->creates a lst that I copied into a CSV file. The lst is also in read_chl_input_lst (if you want to see it), but I saved the file which was a CSV with two
columns, Date and Value. this csv (chl_data_Popof.csv) goes into -> read_chl_Popof_USETHIS.py -> chl_popof.parquet
PAR: https://portal.aoos.org/#metadata/75407/station/data -> PAR-anchor-point-AK.csv ->read_PAR_PopofIsland.py -> PAR_popof.parquet
NO3: to get data, I used NOx graphs that were emailed from Michael Stekoll to Toby and me and used software that turns graphs into data points. I put the data points into CSV files.
CSV files (Kodiak files/env. inputs/NOx INPUTS/) -> read_NO3_math_PopofIsland.py -> NO3_popof.parquet



DATA USED FOR DEB:
PAR: https://portal.aoos.org/#metadata/75407/station/data -> PAR_DEB_2020.csv
NOx: Michael Stekoll graphs from 0,2,5,10 m depths from 2019 -> NOX.csv
CO2/DIC: https://www.ncei.noaa.gov/data/oceans/ncei/ocads/metadata/0219960.html -> determined best year of data and selected it in read_DEB_input_DIC.py -> DIC_valid_data.csv
SST: https://www.ndbc.noaa.gov/station_page.php?station=kdaa2 -> read_SST_NOAA_buoy_KDAA2_data.py -> SST_from_KDAA2{YEAR_CHOICE}-{NEXT_YR_LAST_2_DIGITS}.csv (put in year and next year's last 2 digits)