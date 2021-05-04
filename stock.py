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
    Code = "RMG.L" # EDIT THIS #
elif Code != "":
    print("Company code set: %s\n" %Code)

# Set date range. This gives financial year covering the range specified.
try:
    Start_year = int(input("Enter year for data to start [Default = 2016]:"))
    print("Start year set: %s" %Start_year)
except ValueError:
    print("Start year set: 2016")
    Start_year = 2016 # EDIT THIS #

try:
    End_year = int(input("Enter year for data to end [Default = 2021]:"))
    print("End year set: %s\n" %End_year)
except ValueError:
    print("End year set: 2021\n")
    End_year = 2021 # EDIT THIS #

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


# -----------------------------------------------------------------------------
            # --- PART 1   --- #
# -----------------------------------------------------------------------------


            # ---   PLOT HISTORICAL DATA   --- #
Data.plot()

plt.xlabel("Date", fontsize = 12)
plt.ylabel("Adj. Close, pence", fontsize = 12)
plt.title("%s Historical Prices for %s Fiscal Year(s) %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)

plt.xlim(Start_date, End_date)
plt.tight_layout()
plt.grid()

if Save == True:
    plt.savefig("Figures/%s/%s Historical Prices for %s Fiscal Year(s) %s" \
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
plt.ylabel("Frequency", fontsize = 12)
plt.title("%s Returns for %s Fiscal Year(s) %s" %(Name, Fiscal_year, Quarter), \
    fontsize = 12)

plt.tight_layout()
plt.grid()

if Save == True:
    plt.savefig("Figures/%s/%s Returns for %s Fiscal Year(s) %s" \
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

ax.set_title("QQ Plot of %s Returns for %s Fiscal Year(s) %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)
ax.set_xlabel("Theoretical Quarterues", loc = "right", fontsize = 12)
ax.set_ylabel("Actual Quarterues", loc = "top", fontsize = 12)

sm.qqplot(Returns, dist = stats.norm, loc = Mean, scale = SD, \
    ax = ax, marker = ".", markersize = 6, color = "b")
sm.qqline(ax, line = "45", label = "y = x", linestyle = "--", color = "r")

ax.set_ylim(-0.1, 0.1)
ax.set_xlim(-0.1, 0.1)
plt.tight_layout()
plt.legend(fontsize = 12, loc = 4)
plt.grid()

if Save == True:
    plt.savefig("Figures/%s/QQ Plot of %s Returns for %s Fiscal Year(s) %s" \
        %(Fiscal_year, Name, Fiscal_year, Quarter))
    print("QQ-plot saved.\n")
elif Save == False:
    pass

plt.show()


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
Date_max = Data[Data == max(Data)].index.tolist()[0]
print("The maximum value of the investment was £%s M on the %s" \
    %('%.2f' %Value_max, str(Date_max)[:10]))

# Calculate the min the investment would have been.
Value_min = Value * (min(Data) / Data[0])
Date_min = Data[Data == min(Data)].index.tolist()[0]
print("The minimum the value the investment was £%s M on the %s\n" \
    %('%.2f' %Value_min, str(Date_min)[:10]))

# Here there will be a calculation of how well a principal of £1M will have
# done over the same period considered above, in a savings account. The
# model used will assume continously compounded interest, with an interest rate
# equal to that of the average 12 LIBOR for the time considered.

# This dict holds the 12 month average LIBOR for each month from 2016 to 2020.
# It will be called # upon based on the start date of the imagined investment
# above. This data is obtained from the following website.
# https://www.macrotrends.net/1433/historical-libor-rates-chart
LIBOR = {"2016-01": 0.0114, "2016-02": 0.0118, "2016-03": 0.0121, \
    "2016-04": 0.0123, "2016-05": 0.0134, "2016-06": 0.0123, "2016-07": 0.0143, \
    "2016-08": 0.0156, "2016-09": 0.0155, "2016-10": 0.0158, "2016-11": 0.0164, \
    "2016-12": 0.0169, \
    
    "2017-01": 0.0171, "2017-02": 0.0176, "2017-03": 0.0180, "2017-04": 0.0177, \
    "2017-05": 0.0172, "2017-06": 0.0174, "2017-07": 0.0173, "2017-08": 0.0171, \
    "2017-09": 0.0178, "2017-10": 0.0185, "2017-11": 0.0195, "2017-12": 0.0211, \
    
    "2018-01": 0.0227, "2018-02": 0.0250, "2018-03": 0.0266, "2018-04": 0.0277, \
    "2018-05": 0.0272, "2018-06": 0.0276, "2018-07": 0.0283, "2018-08": 0.0284, \
    "2018-09": 0.0292, "2018-10": 0.0308, "2018-11": 0.0312, "2018-12": 0.0301, \
    
    "2019-01": 0.0298, "2019-02": 0.0287, "2019-03": 0.0271, "2019-04": 0.0272, \
    "2019-05": 0.0251, "2019-06": 0.0218, "2019-07": 0.0219, "2019-08": 0.0197, \
    "2019-09": 0.0203, "2019-10": 0.0196, "2019-11": 0.0195, "2019-12": 0.0200, \
    
    "2020-01": 0.0181, "2020-02": 0.0138, "2020-03": 0.0100, "2020-04": 0.0087, \
    "2020-05": 0.0067, "2020-06": 0.0055, "2020-07": 0.0045, "2020-08": 0.0045, \
    "2020-09": 0.0043}

def cci(P):
# This function calculates the compound interest on a principal after the time
# considered of the whole data set. The inputs are the principle investment
# and R, the rate, taken from the LIBOR dict.
    
    # Calculate the time in years of the data set considered.
    T = (End_date - Start_date).days / 365
    
    # Find the correct LIBOR for the calculation. The LIBOR at the start of the
    # data is taken and assumed to be the same over the entire time.
    R = LIBOR[str(Start_date)[:7]]
    print("Based on 12 month avg. LIBOR in %s the interest rate of savings = %s" \
        %(str(Start_date)[:7], str('%.2f' %(R * 100)) + " %"))
    
    # Calculate the value of an investment after the time considered.
    F = P * np.exp(R * T)
    
    # Return value to user.
    return F

# Calculate the final price of an investment of £1M over the time considered.
# F = cci(Value)
# print("Investing the £%s M from %s to %s would have yielded £%s M\n" \
    # %('%.2f' %Value, Start_date, End_date, '%.2f' %F))


            # ---   PREDICTING FUTURE PRICE PART.1   --- #
print("    # ---   PREDICTING FUTURE PRICE PART.1   --- #")
print("This section utalises a normal distribution model for the data\n")

def dS_norm(Volatility, Drift, S, dt = 1/4, X = 2):
# This function uses the volatility, drift, initial price (pence), confidence 
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

# Calculate the drift and volatility of the daily returns based on a normal
# distribution.
Volatility_n = SD / np.sqrt(1 / 252)
Drift_n = Mean / (1 / 252) - Volatility_n**2 / 2
print("Volatility = %s" %('%.2f' %(Volatility_n * 100) + " %"))
print("Drift = %s\n" %('%.2f' %(Drift_n * 100) + " %"))

# Get latest share price.
S = Data[-1]
print("Share price on %s is %s p" %(End_date, '%.2f' %S))

# Call function to get a prediction for the future share price.
dS_n_upper, dS_n_lower = dS_norm(Volatility_n, Drift_n, S, dt)
print("The predicted share price on %s (%s yrs later) with %s confidence is:" \
    %(End_date + timedelta(dt * 365), dt, "95%"))
print("%s p < S < %s p\n" %('%.2f' %dS_n_lower,'%.2f' %dS_n_upper))


# -----------------------------------------------------------------------------
            # ---   PART 2   --- #
# -----------------------------------------------------------------------------


            # ---   PREDICTING FUTURE PRICE PART.2   --- #
# This section does the same as the previous PREDICTING FUTURE PRICE section,
# however, this one uses a lognormal model for hte data. This will give
# different results for the Drift and future price range. The same dS() function
# can be used just with the new drift and 
print("    # ---   PREDICTING FUTURE PRICE PART.2   --- #")
print("This section utalises a lognormal model for the data\n")


# Create a function to calculate the future price range using a lognorm model.
def dS_lognorm(Volatility, Drift, S, dt = 1/4, X = 2):
# This function uses the volatility, drift, initial price (pence), confidence 
# and a time period (fractions of a year) to estimate the future price of
# the share. The calculation is based on the assumption that the data follows
# a lognormal distribution.

    # Calculate the upper and lower changes in price.
    dS_upper = np.exp(Drift * dt + Volatility * np.sqrt(dt) * X) * S
    dS_lower = np.exp(Drift * dt - Volatility * np.sqrt(dt) * X) * S
    
    # Calculate new price upper and lower limits.
    New_price_upper = S + dS_upper
    New_price_lower = S - dS_lower
    
    # Return upper and lower limit of possible future prices.
    return New_price_upper, New_price_lower


# Calculate Drift of based on a lognormal distribution molde.
Volatility_ln = Volatility_n.copy()
Drift_ln = Drift_n - (Volatility_ln**2 / 2)
print("Volatility using lognorm model = %s" \
    %(str('%.2f' %(Volatility_ln * 100)) + " %"))
print("Drift using lognorm model = %s\n" \
    %(str('%.2f' %(Drift_ln * 100)) + " %"))

# Call function to get a prediction for the future share price.
dS_ln_upper, dS_ln_lower = dS_lognorm(Volatility_ln, Drift_ln, S, dt)
print("The predicted share price on %s (%s yrs later) with %s confidence is:" \
    %(End_date + timedelta(dt * 365), dt, "95%"))
print("%s p < S < %s p\n" %('%.2f' %dS_ln_lower,'%.2f' %dS_ln_upper))


            # ---   EXIT MESSAGE   --- #
# This is so I can run the program by double clicking the file and it doesn't
# close the terminal as soon as it's finished.
Exit = input("Hit ENTER to exit program:")