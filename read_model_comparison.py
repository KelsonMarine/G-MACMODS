'''Compares the DEB model and G-MACMODS for two different years (the SST, PAR, and NOx data is different for the two years, but the other parameters are constant).'''
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import os
print(os.getcwd())

df1 = pd.read_csv("../../code/model comparisons/2021/output with new SST data/DEB_output_to_midjuly2021_KDAA2 buoynew.csv")
df2 = pd.read_csv("../../code/model comparisons/2020/output with new SST data/GMACMODS_output_2019-2020.csv")
df3 = pd.read_csv("../../code/model comparisons/2020/output with new SST data/DEB_output_to_midjuly2020_KDAA2 buoynew.csv")
df4 = pd.read_csv("../../code/model comparisons/2020/output with new SST data/GMACMODS_output_2020-2021.csv")
df1["date"] = pd.to_datetime(df1["date"], errors = "coerce")
df1.set_index("date", inplace = True)
df1 = df1.resample("D").mean()
print(df1)
df3["date"] = pd.to_datetime(df3["date"], errors = "coerce")
df3.set_index("date", inplace = True)
df3 = df3.resample("D").mean()
df2["date"] = pd.to_datetime(df2["date"])
df2["date_aligned"] = df2["date"] - pd.DateOffset(years = 2)
df4["date"] = pd.to_datetime(df4["date"])
df4["date_aligned"] = df4["date"] - pd.DateOffset(years = 1)
plt.plot(df2["date_aligned"], df2["biomass"], color = "green", label = "2019-20 GMACMODS") #gmacmods model
plt.plot(df2["date_aligned"], df4["biomass"], color = "pink", label = "2020-21 GMACMODS")
plt.plot(df1.index, df3["dw"], color = "blue", label = "2019-20 DEB")
plt.plot(df1.index, df1["dw"], color = "red", label = "2020-21 DEB")#DEB model
plt.legend()
plt.ylabel("g dw/ m")
#plt.yscale("log")
#plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b%Y"))
#plt.yticks(np.arange(0,5, step = .2))
plt.grid(True)
#savefig("../../code/model comparisons/using_7g_SST2019-20_vs_2020-21_KDAA2_log.png")
plt.show()