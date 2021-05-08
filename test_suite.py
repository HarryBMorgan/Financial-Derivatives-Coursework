# -----------------------------------------------------------------------------
# Test suite for stuff in the stock.py module.
# Harry Morgan
# -----------------------------------------------------------------------------
# IMPORTS
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# GET DATA
Data = pdr.get_data_yahoo("RMG.L", start = "2016-04-05", \
    end = "2021-04-05")["Adj Close"]

# -----------------------------------------------------------------------------
# TEST SUITE
# The information I've used here was explained in the last 10 inutes of the
# week 7 tutorial video.

# Set time interval as 1 financial day.
T = 1 / 252


# Create normal returns data.
# This is what's done in my spreadsheet.
Returns = []
for i in range(len(Data) - 1):
    Returns.append(Data[i + 1] / Data[i] - 1)

# Print the volatility of this data set.
Volatility = np.std(Returns) / np.sqrt(T) * 100
print("Normal Volatility = %s" %(str('%.2f' %Volatility) + " %"))

# Create drift from normal returns data.
Drift = np.mean(Returns) / T * 100
print("Normal Drift = %s\n" %(str('%.2f' %Drift) + " %"))


# Create log returns data. That's the log of the difference in price from one
# day to the next.
# This is what he does in the Tutorial video.
Log_returns = []
for i in range(len(Data) - 1):
    Log_returns.append(np.log(Data[i + 1] / Data[i]))

# Calculate it's volatility as per and make into %.
Log_volatility = np.std(Log_returns) / np.sqrt(T) * 100
print("Log Volatility = %s" %(str('%.2f' %Log_volatility) + " %"))

# Calculate drift from mean.
Log_drift = (np.mean(Log_returns) + (Log_volatility / 100)**2 / 2) * 100
print("Log Drift = %s\n" %(str('%.2f' %Log_drift) + " %"))