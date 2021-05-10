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
import stock_module as stock
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
Save = stock.get_save()

# Set names of company and it's code.
Name, Code = stock.get_name()

# Set date range. This gives financial year covering the range specified.
Start_date, End_date, Quarter, Fiscal_year = stock.set_dates()


            # ---   GET DATA   --- #
# Get the historical data from Yahoo Finance.
Data = pdr.get_data_yahoo(Code, start = Start_date, end = End_date)["Adj Close"]


            # ---   OPEN LOG FILE   --- #
# Open the file.
File = open("Log.txt", "w+")


# -----------------------------------------------------------------------------
            # ---   PLOTS   --- #
# -----------------------------------------------------------------------------


            # ---   PLOT HISTORICAL DATA   --- #
Data.plot()

plt.xlabel("Date", fontsize = 12)
plt.ylabel("Adj. Close, pence", fontsize = 12)
plt.title("%s Historical Prices for %s %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)

plt.xlim(Start_date, End_date)
plt.tight_layout()
plt.grid()

# Check if user wants to save the figures.
if Save == True:
    plt.savefig("Historical Prices.png")
    print("Historical price plot saved.\n")
elif Save == False:
    pass

plt.show()


            # ---   PLOT RETURNS HISTOGRAM   --- #
# Calculate daily returns. Un-comment the rest to calculate weekly/monthly
# returns. [The returns are the change in price at the end of the day compared
# to the previous day.]
Returns = []
for i in range(len(Data) - 1):
    Returns.append(Data[i + 1] / Data[i] - 1)

# Plot histogram and get number of bins used as a variable.
_, Bins, _ = plt.hist(Returns, bins = 100, density = True, \
    label = "Daily Returns")

# Calculate the standard deviation and mean of the returns.
Mean, SD = stats.norm.fit(Returns)

# Generate Line Of Best Fit and plot it.
Bin_centres = Bins[:-1] + np.diff(Bins) / 2
plt.plot(Bin_centres, stats.norm.pdf(Bin_centres, Mean, SD), \
    label = "Fitted Distribution")

# Format plot.
plt.xlabel("Daily returns %", fontsize = 12)
plt.ylabel("Frequency", fontsize = 12)
plt.title("%s Returns for %s %s" %(Name, Fiscal_year, Quarter), \
    fontsize = 12)

plt.legend(fontsize = 12)
plt.tight_layout()
plt.grid()

# Check if user wants to save the figures.
if Save == True:
    plt.savefig("Returns.png")
    print("Histogram saved.\n")
elif Save == False:
    pass

plt.show()


            # ---   QQ PLOT   --- #
# This Quantile-Quantile plot is to check how well the data fit a normal 
# distribution.
ax = plt.gca()
ax.set_title("QQ Plot of %s Returns for %s %s" \
    %(Name, Fiscal_year, Quarter), fontsize = 12)
plt.xlabel("Theoretical", fontsize = 12)
plt.ylabel("Sample", fontsize = 12)

sm.qqplot(np.array(Returns), dist = stats.norm, loc = Mean, scale = SD, \
    ax = ax, marker = ".", markersize = 6, color = "b")
sm.qqline(ax, line = "45", label = "y = x", linestyle = "--", color = "r")

plt.tight_layout()
plt.legend(fontsize = 12, loc = 4)
plt.grid()

# Check if user wants to save the figures.
if Save == True:
    plt.savefig("QQ-Plot.png")
    print("QQ-plot saved.\n")
elif Save == False:
    pass

plt.show()


# -----------------------------------------------------------------------------
            # ---   INVESTMENT SCENARIO   --- #
# -----------------------------------------------------------------------------

stock.log(File, "    # ---   INVESTMENT SCENARIO   --- #")
Run = input("Hit ENTER to run Investment Scenario:\n")
# Here the code to print information about an initial £1M investment on the
# Start_date will be considered. Information calculated will include the value
# of the investment today, the return (%) over the period considered, the
# maximum and minimum values of the investment ofer the period. Comparison data
# will also be calculated which will be explained in due course.

# Create initial investment on Start_date.
Value = 1 #Million british pounds.
stock.log(File, \
    "Considering a £%s M investment over the time range specified:\n" %Value)
stock.log(File, "Value of investment on %s = £%s M" %(Start_date, '%.2f' %Value))

# Calculate change over time range considered.
Change = Data[-1] / Data[0]
Value_final = Value * Change
stock.log(File, "Value of investment on %s = £%s M\n" \
    %(End_date, '%.2f' %Value_final))

# Calculate the max the investment would have been.
Value_max = Value * (max(Data) / Data[0])
Date_max = Data[Data == max(Data)].index.tolist()[0]
stock.log(File, "The maximum value of the investment was £%s M on the %s" \
    %('%.2f' %Value_max, str(Date_max)[:10]))

# Calculate the min the investment would have been.
Value_min = Value * (min(Data) / Data[0])
Date_min = Data[Data == min(Data)].index.tolist()[0]
stock.log(File, "The minimum the value the investment was £%s M on the %s\n" \
    %('%.2f' %Value_min, str(Date_min)[:10]))

# Here there will be a calculation of how well a principal of £1M will have
# done over the same period considered above, in a savings account. The
# model used will assume continously compounded interest, with an interest rate
# equal to that of the average 12 LIBOR for the time considered.

# Calculate the final price of an investment of £1M over the time considered.
F, R = stock.cc_interest(Value, Start_date, End_date, Quarter)
stock.log(File, "Based on 12 month avg. LIBOR the interest rate of savings = %s" \
    %(str('%.5f' %(R * 100)) + " %"))
stock.log(File, "Investing the £%s M from %s to %s would have yielded £%s M\n" \
    %('%.2f' %Value, Start_date, End_date, '%.2f' %F))


# -----------------------------------------------------------------------------
            # ---   PREDICTING FUTURE PRICE   --- #
# -----------------------------------------------------------------------------

            # ---   PREDICTING FUTURE PRICE PART.1   --- #
stock.log(File, "    # ---   PREDICTING FUTURE PRICE PART.1   --- #")
Run = input("Hit ENTER to run Predicting Future Price Part.1:\n")
stock.log(File, "This section utalises a normal distribution model for the data\n")

# Set time frame to calculate for.
dt = 2 / 12
stock.log(File, "Calculating for %s years in the future\n" %('%.4f' %dt))

# Calculate the drift and volatility of the daily returns based on a normal
# distribution.
Norm_vol, Norm_drift = stock.get_vol_drift(Mean, SD)
stock.log(File, "Volatility using normal model = %s" \
    %('%.2f' %(Norm_vol * 100) + " %"))
stock.log(File, "Drift using normal model = %s" \
    %('%.2f' %(Norm_drift * 100) + " %\n"))


# Get latest share price.
S = Data[-1]
stock.log(File, "Share price on %s is %s p" %(End_date, '%.2f' %S))

# Call function to get a prediction for the future share price.
Norm_upper, Norm_lower = stock.ds(Volatility = Norm_vol, Drift = Norm_drift, \
    S = S, dt = dt)

# Print the results to the user.
stock.log(File, \
    "The predicted share price on %s (%s yrs later) with %s confidence is:" \
    %(End_date + timedelta(days = dt * 365), ('%.2f' %dt), "95%"))
stock.log(File, "%s p < S < %s p\n" %('%.2f' %Norm_lower,'%.2f' %Norm_upper))


            # ---   PREDICTING FUTURE PRICE PART.2   --- #
stock.log(File, "    # ---   PREDICTING FUTURE PRICE PART.2   --- #")
Run = input("Hit ENTER to run Predicting Future Price Part.1:\n")
stock.log(File, "This section utalises a lognormal model for the data\n")

# This section does the same as the previous PREDICTING FUTURE PRICE section,
# however, this one uses a lognormal model for the data. This will give
# different results for the Drift and future price range. The same dS() function
# can be used just with the new drift and volatility. Make sure to specify the
# distribution type when calling, otherwise the default "norm" will be used.

# Calculate Drift of based on a lognormal distribution molde.
Log_returns = []
for i in range(len(Data) - 1):
    Log_returns.append(np.log(Data[i + 1] / Data[i]))

Log_mean = np.mean(Log_returns)
Log_sd = np.std(Log_returns)

Log_vol, Log_drift = stock.get_vol_drift(Log_mean, Log_sd, dist_type = "lognorm")
stock.log(File, "Volatility using lognormal model = %s" \
    %('%.2f' %(Log_vol * 100)))
stock.log(File, "Drift using lognormal model = %s" \
    %('%.2f' %(Log_drift * 100) + " %\n"))


# Call function to get a prediction for the future share price.
Log_upper, Log_lower = stock.ds(Volatility = Log_vol, Drift = Log_drift, \
    S = S, dt = dt, dist_type = "lognorm")

# Print results to the user.
stock.log(File, \
    "The predicted share price on %s (%s yrs later) with %s confidence is:" \
    %(End_date + timedelta(dt * 365), ('%.2f' %dt), "95%"))
stock.log(File, "%s p < S < %s p\n" %('%.2f' %Log_lower,'%.2f' %Log_upper))


# -----------------------------------------------------------------------------
            # ---   EXIT MESSAGE   --- #
# -----------------------------------------------------------------------------

# Close the file.
File.close()

# This is so I can run the program by double clicking the file and it doesn't
# close the terminal as soon as it's finished.
Exit = input("Hit ENTER to exit program:")