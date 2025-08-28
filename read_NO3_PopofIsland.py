'''This found that the ratio between nitrate: nitrate+nitrite is .97 and all of the results were within .015 of that for the months studied
https://scholarworks.alaska.edu/bitstream/handle/11122/15461/Bloch_D_2024.pdf?sequence=1&isAllowed=y'''

import pandas as pd
df = pd.read_csv("../Kodiak files/env. inputs/nitrate nitrite data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index("Date")
nitrate_monthly_avg = df["Nitrate"].resample("MS").mean()
nitrite_monthly_avg = df["Nitrite"].resample("MS").mean()
ratio = nitrate_monthly_avg / (nitrate_monthly_avg + nitrite_monthly_avg)
print(ratio) #if you average these values you get .97