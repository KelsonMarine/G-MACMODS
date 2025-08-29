# G-MACMODS
Global MacroAlgae Cultivation MODeling System (G-MACMODS)
============================================================================
Isabella Arzeno-Soltero
Benjamin T. Saenz
Kristen Davis

Edited by Alex + Greta

Updated: 2025-08-26

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