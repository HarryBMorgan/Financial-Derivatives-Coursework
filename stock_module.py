# -----------------------------------------------------------------------------
# Finance Coursework
# Harry Morgan
# -----------------------------------------------------------------------------
            # ---   PROGRAM DESCRIPTION   --- #
# This program holds the modules required for the stock.py program. It's main
# use is cleaning up the main (stock.py) program. It should als help me with
# debugging as it'll be better organised this way.


            # ---   IMPORTS   --- #
from datetime import date, timedelta
import numpy as np


            # ---   SET VARIABLES   --- #
# This is just so you can experiment without overwriting data you have already
# generated. Switch to True when you want to save the figures generated.
def get_save():
    Save_in = str(input("Save the figures? (y/n)? [Default = n]"))
    if Save_in.lower() == "y":
        print("Saving preference set: Saving plots\n")
        Save = True
    else:
        print("Saving preference set: Not saving plots\n")
        Save = False

    return Save

# Set names of company and it's code.
def get_name():
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
    
    return Name, Code

# Set date range. This gives financial year covering the range specified.
def set_dates():
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

    # Produce the string for graphs that is the Financial year in question.
    Fiscal_year = "%s-%s" %(Start_year, End_year - 2000)
    
    # Set the quarter of the time period.
    Start_date, End_date, Quarter = __set_quarter__(Start_year, End_year)
    
    return Start_date, End_date, Quarter, Fiscal_year

# Set which quarter to use. Leave empty if want whole year.
# This is a sub-function used within the set_years() function. It is not
# callable by the user.
def __set_quarter__(Start_year, End_year):
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

    return Start_date, End_date, Quarter

# Ask for time frame to calculate for.
def get_dt():
    try:
        dt = float(input("Enter fraction of year to predict ahead [Default = 1/4]:"))
        print("Time ahead set at %s yrs\n" %dt)
    except ValueError:
        dt = 1/4
        print("Time period set: %s yrs\n" %dt)

    return dt

# Calculates the volatility depending on the type of model, norm or lognorm.
def get_vol_drift(mu, sigma, T = 1 / 250, dist_type = "norm"):
    if dist_type == "norm":
        Vol = sigma / np.sqrt(T)
        Drift = mu / T
        
    elif dist_type == "lognorm":
        Vol = sigma / np.sqrt(T)
        Drift = mu + (Vol**2 / 2)
        
    print("Volatility using %s model = %s" \
        %(dist_type, '%.2f' %(Vol * 100) + " %"))
    print("Drift using %s model = %s" \
        %(dist_type, '%.2f' %(Drift * 100) + " %\n"))

    return Vol, Drift

# This function uses the volatility, drift, initial price (pence), confidence 
# and a time period (fractions of a year) to estimate the future price of
# the share. The calculation is based on the assumption that the data follows
# a normal distribution.
def ds(Volatility, Drift, S, dt = 1/4, X = 2, dist_type = "norm"):
    if dist_type == "norm":
        # Calculate the upper and lower changes in price.
        dS_upper = Drift * S * dt + Volatility * S * np.sqrt(dt) * X
        dS_lower = Drift * S * dt - Volatility * S * np.sqrt(dt) * X
        
    elif dist_type == "lognorm":
        # Calculate the upper and lower changes in price.
        dS_upper = np.exp(Drift * dt + Volatility * np.sqrt(dt) * X) * S
        dS_lower = np.exp(Drift * dt - Volatility * np.sqrt(dt) * X) * S
    
    # Calculate new price upper and lower limits.
    New_price_upper = S + dS_upper
    New_price_lower = S - dS_lower

    # Return upper and lower limit of possible future prices.
    return New_price_upper, New_price_lower

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

# This function calculates the compound interest on a principal after the time
# considered of the whole data set. The inputs are the principle investment
# and R, the rate, taken from the LIBOR dict.
def cc_interest(P, Start_date, End_date):

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