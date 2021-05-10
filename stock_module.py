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
        Start_year = int(input("Enter year of data to cover [Default = 2016]:"))
        print("Start year set: %s" %Start_year)
    
    except ValueError:
        print("Start year set: 2016")
        Start_year = 2016 # EDIT THIS #

    try:
        End_year = int(input("Enter year for data to end [Default = 2020]:"))
        print("End year set: %s\n" %End_year)
    
    except ValueError:
        print("End year set: 2020\n")
        End_year = 2020 # EDIT THIS #

    # Set the quarter of the time period.
    Start_date, End_date, Quarter = __set_quarter__(Start_year, End_year)
    
    # Produce the string for graphs that is the Financial year in question.
    Fiscal_year = "%s.%s.%s - %s.%s.%s" \
        %(Start_date.day, Start_date.month, Start_date.year, \
        End_date.day, End_date.month, End_date.year)
    
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
    End_date = date(End_year, 12, 31) - timedelta(days = val[0] * 365)
    Start_date = date(Start_year, 1, 1) + timedelta(days = val[1] * 356)

    return Start_date, End_date, Quarter

# Calculates the volatility depending on the type of model, norm or lognorm.
def get_vol_drift(mu, sigma, T = 1 / 252, dist_type = "norm"):
    if dist_type == "norm":
        Vol = sigma / np.sqrt(T)
        Drift = mu / T
        
    elif dist_type == "lognorm":
        Vol = sigma / np.sqrt(T)
        Drift = mu + (Vol**2 / 2)
    
    return Vol, Drift

# This function uses the volatility, drift, initial price (pence), confidence 
# and a time period (fractions of a year) to estimate the future price of
# the share. The calculation is based on the assumption that the data follows
# a normal distribution.
def ds(Volatility, Drift, S, dt = 1/6, X = 2, dist_type = "norm"):
    if dist_type == "norm":
        # Calculate the upper and lower changes in price.
        a = Drift * dt * S
        b = Volatility * np.sqrt(dt) * X * S
        New_price_upper = S + a + b
        New_price_lower = S + a - b
        
    elif dist_type == "lognorm":
        # Calculate the upper and lower changes in price.
        a = (Drift - (Volatility**2 / 2)) * dt
        b = Volatility * np.sqrt(dt) * X
        dS_upper = np.log(S) + a + b
        dS_lower = np.log(S) + a - b
        New_price_upper = np.exp(dS_upper)
        New_price_lower = np.exp(dS_lower)
    
    # Calculate new price upper and lower limits.


    # Return upper and lower limit of possible future prices.
    return New_price_upper, New_price_lower

# This dict holds the 12 month average LIBOR for each month from 2016 to 2020.
# It will be called # upon based on the start date of the imagined investment
# above. This data is obtained from the following website.
# https://www.macrotrends.net/1433/historical-libor-rates-chart
LIBOR = {"2016-2020": 0.0081146, "2016-2016": 0.0089053, "2017-2017": 0.0070344, \
        "2018-2018": 0.0099647, "2019-2019": 0.0100077, "2020-2020": 0.0046735, \
        "2020-2020first quarter": 0.0081448, "2020-2020second quarter": 0.0066524, \
        "2020-2020third quarter": 0.0026382, "2020-2020fourth quarter": 0.0012389}

# This function calculates the compound interest on a principal after the time
# considered of the whole data set. The inputs are the principle investment
# and R, the rate, taken from the LIBOR dict.
def cc_interest(P, Start_date, End_date, Quarter):

    # Calculate the time in years of the data set considered.
    T = (End_date - Start_date).days / 365
    
    # Find the correct LIBOR for the calculation. The LIBOR at the start of the
    # data is taken and assumed to be the same over the entire time.
    R = LIBOR[str(Start_date.year) + "-" + str(End_date.year) + Quarter]
    
    # Calculate the value of an investment after the time considered.
    F = P * np.exp(R * T)
    
    # Return value to user.
    return F, R

# This function writes information to the screen and logs it to the file.
def log(File, Text):
    # Print the information to the user.
    print(Text)
    
    # Write information to the File.
    File.write(Text + "\n")