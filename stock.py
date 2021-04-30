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


            # ---   SET VARIABLES   --- #
print("    # ---   SET VARIABLES   --- #\n")

# This is just so you can experiment without overwriting data you have already
# generated. Switch to True when you want to save the figures generated.
Save_in = str(input("Save the figures? (y/n)? [Default = n]"))
if Save_in.lower() == "y":
    print("Saving preference set: Saving plots\n")
    Save = True
else:
    print("Saving preference set: Not saving plots\n")
    Save = False

# Set names of company and it's code.
Name = str(input("Enter name of company [Default = Royal Mail]:")).capitalize()
if Name == "":
    print("Company set: Royal Mail")
    Name = "Royal Mail" # EDIT THIS #
    Code = "RMG.L" # EDIT THIS #
elif Name != "":
    print("Company set: %s" %Name)
    Code = str(input("Enter stock code [Default = RMG.L]:")).upper()

if Code == "":
    print("Company code set: RMG.L\n")
    Code = "RMG.L"
elif Code != "":
    print("Company code set: %s\n" %Code)

# Set date range. This gives financial year covering the range specified.
try:
    Start_year = int(input("Enter year for data to start [Default = 2016]:"))
    print("Start year set: %s" %Start_year)
except ValueError:
    print("Start year set: 2016")
    Start_year = 2016

try:
    End_year = int(input("Enter year for data to end [Default = 2021]:"))
    print("End year set: %s\n" %End_year)
except ValueError:
    print("End year set: 2021\n")
    End_year = 2021

Fiscal_year = "%s-%s" %(Start_year, End_year - 2000)

# Set which quarter to use. Leave empty if want whole year.
Quarter_dict = {"firstquarter": [3/4, 0], "secondquarter": [2/4, 1/4], \
    "thirdquarter": [1/4, 2/4], "fourthquarter": [0, 3/4], "": [0, 0]}

try:
    Quarter = str(input("Enter quarter [Default = Whole Year]:"))
    val = Quarter_dict[Quarter.lower().replace(" ", "")]
    if Quarter == "":
        print("Qurter set: Whole Year\n")
    elif Quarter != "":
        print("Quarter set: %s\n" %Quarter)
except KeyError:
    val = Quarter_dict[""]
    print("Quarter set: Whole Year\n")

# Set start and end dates for time period. This covers from April to April
# (fiscal year).
End_date = date(End_year, 4, 5) - timedelta(val[0] * 365)
Start_date = date(Start_year, 4, 5) + timedelta(val[1] * 356)


            # ---   GET DATA   --- #
# Get the historical data from Yahoo Finance.
Data = pdr.get_data_yahoo(Code, start = Start_date, end = End_date)["Adj Close"]


            # ---   PLOT HISTORICAL DATA   --- #
Data.plot()
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
Returns = Data.pct_change()#.resample("W").ffill().pct_change()

# Calculate the standard deviation and mean of the returns. This is used to
# calculate the volatility and drift.
SD = np.std(Returns)
Mean = np.mean(Returns)

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
ax = plt.gca()

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


            # ---   PREDICTING FUTURE PRICE   --- #
print("    # ---   PREDICTING FUTURE PRICE   --- #\n")

def dS(Volatility, Drift, S, X = 2, dt = 1/4):
# This function used the volatility, drift, initial price (pence), confidence 
# and a time period (fractions of a year) to estimate the future price of
# the share. The calculation is based on the assumption that the data follows
# a normal distribution.

    # Calculate the upper and lower changes in price.
    dS_upper = Drift * S * dt + Volatility * S * np.sqrt(dt) * X
    dS_lower = Drift * S * dt - Volatility * S * np.sqrt(dt) * X
    
    # Calculate new price upper and lower limits.
    New_price_upper = S + dS_upper
    New_price_lower = S - dS_lower
    
    # Return upper and lower limit of possible future prices.
    return New_price_upper, New_price_lower

# Ask for time frame to calculate for.
try:
    dt = float(input("Enter fraction of year to predict ahead [Default = 1/4]:"))
    print("Time ahead set at %s yrs\n" %dt)
except ValueError:
    dt = 1/4
    print("Time period set: %s yrs\n" %dt)

# Set the timescale to use in calculations. This is 1 day of a fiscal year.
T = 1 / 252

# Calculate the drift and volatility of the daily returns based on a normal
# distribution.
Volatility = SD / np.sqrt(T)
Drift = Mean / T - Volatility**2 / 2
print("Volatility =", Volatility)
print("Drift =", Drift, "\n")

# Get latest share price.
S = Data[-1]
print("Share price on %s is %s p" %(End_date, '%.2f' %S))

# Call function to get a prediction for the future share price.
dS_upper, dS_lower = dS(Volatility, Drift, S, dt = dt)
print("The predicted share price on %s (%s yrs later) with %s confidence is:" \
    %(End_date + timedelta(dt * 365), dt, "95%"))
print("%s p < S < %s p\n" %('%.2f' %dS_lower,'%.2f' %dS_upper))


            # ---   INVESTMENT SCENARIO   --- #
print("    # ---   INVESTMENT SCENARIO   --- #\n")
# Here the code to print information about an initial £1M investment on the
# Start_date will be considered. Information calculated will include the value
# of the investment today, the return (%) over the period considered, the
# maximum and minimum values of the investment ofer the period. Comparison data
# will also be calculated which will be explained in due course.

# Create initial investment on Start_date.
Value = 1 #Million british pounds.
print("Considering a £%s M investment over the time range considered:\n" %Value)
print("Value of investment on %s = £%s M" %(Start_date, '%.2f' %Value))

# Calculate change over time range considered.
Change = Data[-1] / Data[0]
Value_final = Value * Change
print("Value of investment on %s = £%s M\n" %(End_date, '%.2f' %Value_final))

# Calculate the max the investment would have been.
Value_max = Value * (max(Data) / Data[0])
Date_max = Data[ Data == max( Data ) ].index.tolist()[0]
print("The maximum value of the investment was £%s M on the %s" \
    %('%.2f' %Value_max, str(Date_max)[:10]))

# Calculate the min the investment would have been.
Value_min = Value * (min(Data) / Data[0])
Date_min = Data[ Data == min( Data ) ].index.tolist()[0]
print("The minimum the value the investment was £%s M on the %s\n" \
    %('%.2f' %Value_min, str(Date_min)[:10]))


            # ---   EXIT MESSAGE   --- #
# This is so I can run the program by double clicking the file and it doesn't
# close the terminal as soon as it's finished.
Exit = input("Hit ENTER to exit program:")