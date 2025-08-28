'''This compares the DEB model environmental parameters, using a multiplier to demonstrate the effect of the parameters
on the model.'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#FOR NOx
df1 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/nox/2019-20/DEB_output_to_midjuly2020_using 1x nox.csv")
df2 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/nox/2019-20/DEB_output_to_midjuly2020_using 0.5x nox.csv")
df3 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/nox/2019-20/DEB_output_to_midjuly2020_using 1.5x nox.csv")
for df in [df1, df2, df3]:
    df["date"] = pd.to_datetime(df["date"], format = "mixed")
    df.set_index("date", inplace = True)
fig, ax = plt.subplots(figsize = (12, 6))
ax.plot(df1.index, df1["dw"], color = "red", label = "baseline nox")
ax.plot(df2.index, df2["dw"], color = "blue", label = "0.5 * nox")
ax.plot(df3.index, df3["dw"], color = "pink", label = "1.5 * nox")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
plt.title("comparison of NOx values and biomass outputs")
plt.ylabel("g dw/ m")
plt.legend()
plt.grid()
#plt.yscale("log")
plt.savefig("../../code/model comparisons/changing inputs comparing outputs/nox/2019-20/DEB nox comparison.png")
plt.show()

#FOR PAR
df4 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/par/2019-20/DEB_output_to_midjuly2020_using 1x par.csv")
df5 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/par/2019-20/DEB_output_to_midjuly2020_using .5x par.csv")
df6 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/par/2019-20/DEB_output_to_midjuly2020_using 1.5x par.csv")
for df in [df4, df5, df6]:
    df["date"] = pd.to_datetime(df["date"], format = "mixed")
    df.set_index("date", inplace = True)
fig, ax = plt.subplots(figsize = (12, 6))
ax.plot(df4.index, df4["dw"], color = "red", label = "baseline PAR")
ax.plot(df5.index, df5["dw"], color = "blue", label = "0.5 * PAR")
ax.plot(df6.index, df6["dw"], color = "pink", label = "1.5 * PAR")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
plt.title("comparison of PAR values and biomass outputs")
plt.ylabel("g dw/ m")
plt.legend()
plt.grid()
#plt.yscale("log")
plt.savefig("../../code/model comparisons/changing inputs comparing outputs/par/2019-20/DEB par comparison.png")
plt.show()

#FOR CO2
df7 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/co2/2019-20/DEB_output_to_midjuly2020_using 1x co2.csv")
df8 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/co2/2019-20/DEB_output_to_midjuly2020_using .5x co2.csv")
df9 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/co2/2019-20/DEB_output_to_midjuly2020_using 1.5x co2.csv")
for df in [df7, df8, df9]:
    df["date"] = pd.to_datetime(df["date"], format = "mixed")
    df.set_index("date", inplace = True)
fig, ax = plt.subplots(figsize = (12, 6))
ax.plot(df7.index, df7["dw"], color = "red", label = "baseline CO2")
ax.plot(df8.index, df8["dw"], color = "blue", label = "0.5 * CO2")
ax.plot(df9.index, df9["dw"], color = "pink", label = "1.5 * CO2")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
plt.title("comparison of CO2 values and biomass outputs")
plt.ylabel("g dw/ m")
plt.legend()
plt.grid()
#plt.yscale("log")
plt.savefig("../../code/model comparisons/changing inputs comparing outputs/co2/2019-20/DEB co2 comparison.png")
plt.show()

#FOR SST
df10 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/sst/2019-20/DEB_output_to_midjuly2020_using +1deg sst.csv")
df11 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/sst/2019-20/DEB_output_to_midjuly2020_using +2deg sst.csv")
df12 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/sst/2019-20/DEB_output_to_midjuly2020_using 1x sst.csv")
df13 = pd.read_csv("../../code/model comparisons/changing inputs comparing outputs/sst/2019-20/DEB_output_to_midjuly2020_using -1deg sst.csv")
for df in [df10, df11, df12, df13]:
    df["date"] = pd.to_datetime(df["date"], format = "mixed")
    df.set_index("date", inplace = True)
fig, ax = plt.subplots(figsize = (12, 6))
ax.plot(df10.index, df10["dw"], color = "red", label = "SST +1 degree C")
ax.plot(df11.index, df11["dw"], color = "blue", label = "SST +2 degrees C")
ax.plot(df12.index, df12["dw"], color = "pink", label = "baseline SST")
ax.plot(df13.index, df13["dw"], color = "green", label = "SST -1 degree C")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
plt.title("comparison of SST values and biomass outputs")
plt.ylabel("g dw/ m")
plt.legend()
plt.grid()
#plt.yscale("log")
plt.savefig("../../code/model comparisons/changing inputs comparing outputs/sst/2019-20/DEB sst comparison.png")
plt.show()