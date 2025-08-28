'''Uses graphs sent to us by Michael Stekoll measured at the site in this paper:
https://onlinelibrary.wiley.com/doi/10.1111/jwas.70017
.97 comes from math on nitrate/nitrite proportions from table in here: https://scholarworks.alaska.edu/bitstream/handle/11122/15461/Bloch_D_2024.pdf?sequence=1&isAllowed=y
concentrations are in uM.'''
NITRATE_RATIO = .97
import pandas as pd
import matplotlib.pyplot as plt
df1 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2019-20_0meters.csv")
df2 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2019-20_2meters.csv")
df3 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2019-20_5meters.csv")
df4 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2019-20_10meters.csv")
df5 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2020-21_2meters.csv")
df6 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2020-21_5meters.csv")
df7 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2020-21_10meters.csv")
df8 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2021-22_2m.csv")
df9 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2021-22_5meters.csv")
df10 = pd.read_csv("../Kodiak files/env. inputs/NOx INPUTS/2021-22_10m.csv")
all_rows = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10])
all_rows["Nox"] = all_rows["Nox"] * NITRATE_RATIO #this is assuming NOx is only NO2 and NO3, and using the percentage of that that is usually nitrate (from the Bloch paper and read_NO3_PopofIsland.py)
all_rows["Date"] = pd.to_datetime(all_rows["Date"])
daily_avg_nox = all_rows.groupby("Date").mean()
# all_rows = daily_avg_nox.set_index("Date")
print(daily_avg_nox)
daily_avg_nox.to_parquet("Popof input data/NO3_popof.parquet")
fig, ax = plt.subplots()
plt.scatter(daily_avg_nox.index, daily_avg_nox)
plt.xlabel("time")
plt.ylabel("uM")
plt.title("Nitrate concentrations unaveraged")
ax.set_xticks([pd.Timestamp("2019-01-01"), pd.Timestamp("2020-01-01"), pd.Timestamp("2021-01-01"), pd.Timestamp("2022-01-01")])

plt.savefig("../Kodiak files/Plots/nitrate_unaveraged.png")
plt.show()

