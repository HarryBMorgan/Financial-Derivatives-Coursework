# -----------------------------------------------------------------------------
# Finance Coursework
# Harry Morgan
# -----------------------------------------------------------------------------
            # --- PROGRAM DESCRIPTION   --- #
# Tihs program prints graphs of the historical adjusted closing price of the
# stock specified by Name and Code. The Date range is given by Start_year and
# End_year. A histogram of the daily returns over this period is given and
# a normal distribution fitted. The validity of the fit is checked using a
# qq-plot. A quarter in a year range can be specified in the Quarter parameter.

# Only edit the fields marked with # EDIT THIS #.


            # ---   IMPORT MODULES   --- #
from datetime import date, timedelta
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm

            # ---   SAVE FIGURES?   --- #
# This is just so you can experiment without overwriting data you have already
# generated. Switch to True when you want to save the figures generated.
Save_in = str(input("Save the figures? (y/n)? [Default = n]"))
if Save_in.lower() == "y":
    print("Program will save plots\n")
    Save = True
else:
    print("Default: Program will not save plots\n")
    Save = False


            # ---   SET VARIABLES   --- #
# Set names of company and it's code.
Name = str(input("Enter name of company [Default = Royal Mail]:")).capitalize()
if Name == "":
    print("Default: Royal Mail")
    Name = "Royal Mail" # EDIT THIS #
    Code = "RMG.L" # EDIT THIS #
elif Name != "":
    print("Company set: %s" %(Name))
    Code = str(input("Enter stock code [Default = RMG.L]:")).upper()

if Code == "":
    print("Default [RMG.L]\n")
    Code = "RMG.L"
elif Code != "":
    print("Company code set: %s\n" %(Code))

# Set date range. This gives financial year covering the range specified.
try:
    Start_year = int(input("Enter year for data to start [Default = 2016]:"))
    print("Start year set: %s" %(Start_year))
except ValueError:
    print("Default: 2016")
    Start_year = 2016

try:
    End_year = int(input("Enter year for data to end [Default = 2021]:"))
    print("End year set: %s\n" %(End_year))
except ValueError:
    print("Default: 2021\n")
    End_year = 2021

Fiscal_year = "%s-%s" %(Start_year, End_year - 2000)

# Set which quarter to use. Leave empty if want whole year.
Quarter = str(input("Enter quarter [Default = Whole Year]:")).lower().strip()
if Quarter != "":
    print("%s selected\n" %(Quarter))
else:
    print("Whole year selected\n")

Quarter_dict = {"firstquarter": [3/4, 0], "secondquarter": [2/4, 1/4], \
    "thirdquarter": [1/4, 2/4], "fourthquarter": [0, 3/4], "": [0, 0]}
val = Quarter_dict[Quarter]

# Set the dates of when to get the data from.
End_date = date(End_year, 4, 5) - timedelta(val[0] * 365)
Start_date = date(Start_year, 4, 5) + timedelta(val[1] * 356)

# Set the timescale.
T = 1 / 250

            # ---   GET DATA   --- #
# Get the historical data from Yahoo Finance.
Data = pdr.get_data_yahoo(Code, start = Start_date, end = End_date)


            # ---   PLOT HISTORICAL DATA   --- #
Data['Adj Close'].plot()
plt.xlabel("Date", fontsize = 12)
plt.xlim(Start_date, End_date)
plt.ylabel("Adj. Close, pence", fontsize = 12)
plt.title("%s Historical Prices for %s Fiscal Year %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)
plt.tight_layout()
plt.grid()
if Save == True:
    plt.savefig("Figures/%s/%s Historical Prices for %s Fiscal Year %s" \
        %(Fiscal_year, Name, Fiscal_year, Quarter))
    print("Historical price plot saved.\n")
elif Save == False:
    pass
plt.show()


            # ---   PLOT RETURNS HISTOGRAM   --- #
# Calculate daily returns. Un-comment the rest to calculate weekly/monthly
# returns. [The returns are the change in price at the end of the day compared
# to the previous day.]
Returns = Data["Adj Close"].pct_change()#.resample("W").ffill().pct_change()

# Calculate the standard deviation and mean of the returns. This is used to
# calculate the volatility and drift.
SD = np.std(Returns)
Mean = np.mean(Returns)
Volatility = SD / np.sqrt(T)
Drift = Mean / T - Volatility**2 / 2
print("Volatility =", Volatility)
print("Drift =", Drift, "\n")

# Use the volatility and drift to create a normal distribution and plot over
# histogram to check how well it fits.
Domain = np.linspace(-0.2, 0.2, len(Returns))
plt.plot(Domain, stats.norm.pdf(Domain, Mean, SD))
Returns.plot.hist(bins = 60, density = True)
plt.xlabel("Daily returns %", fontsize = 12)
plt.title("%s Returns for %s Fiscal Year %s" %(Name, Fiscal_year, Quarter), \
    fontsize = 12)
plt.tight_layout()
plt.grid()
if Save == True:
    plt.savefig("Figures/%s/%s Returns for %s Fiscal Year %s" \
        %(Fiscal_year, Name, Fiscal_year, Quarter))
    print("Histogram saved.\n")
elif Save == False:
    pass
plt.show()


            # ---   QQ PLOT   --- #
# This Quantile-Quantile plot is to check how well the data fit a normal 
# distribution.
ax = plt.gca()  #Alter the spines to make the graph nicer to look at.

ax.spines["bottom"].set_position(("data", 0.0))
ax.spines["left"].set_position(("data", 0.0))
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.set_title("QQ Plot of %s Returns for %s Fiscal Year %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)
ax.set_xlabel("Theoretical Quarterues", loc = "right", fontsize = 12)
ax.set_ylabel("Actual Quarterues", loc = "top", fontsize = 12)

ax.set_ylim(-0.2, 0.3)

sm.qqplot(Returns, loc = Mean, scale = SD, ax = ax, marker = ".", \
    markersize = 6, color = "b")
sm.qqline(ax, line = "45", label = "y = x", linestyle = "--", color = "r")

plt.tight_layout()
plt.legend(fontsize = 12, loc = 4)
plt.grid()
if Save == True:
    plt.savefig("Figures/%s/QQ Plot of %s Returns for %s Fiscal Year %s" \
        %(Fiscal_year, Name, Fiscal_year, Quarter))
    print("QQ-plot saved.\n")
elif Save == False:
    pass
plt.show()


            # ---   SOMETHING NEW   --- #
# This is where I will add new code in the future.


            # ---   EXIT MESSAGE   --- #
# This is so I can run the program by double clicking the file and it doesn't
# close the terminal as soon as it's finished.
Exit = input("Hit ENTER to exit program:")