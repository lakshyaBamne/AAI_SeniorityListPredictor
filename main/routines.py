# libraries required
from datetime import date, timedelta

#########################################################################
# module to store all the functions used in the program
#########################################################################

# Function to check if a given year is a leap year or not
# Function returns 1 if true else false
def _IsLeapYear_(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return 1
            else:
                return 0
        else:
             return 1
    else:
        return 0

#########################################################################

# Function taken in input a date object
# returns the date which is the next month's end date
# parameter is a datetime.date object and has attributes like month, year, day
def _NextEndOFMonth_(curr_date):
    # variable which tells how many days should be added to get the 
    # next end of month date
    next_eom = None

    # if curr Date is Jan 31
    if curr_date.month == 1:
        if _IsLeapYear_(curr_date.year)==1:
            next_eom = 29
        else:
            next_eom = 28
    if curr_date.month in [3,5,8,10]:
        next_eom = 30
    if curr_date.month in [2,4,6,7,9,11,12]:
        next_eom = 31
    
    # adding the required days to get the next end of month date
    next_date = curr_date + timedelta(days=next_eom)

    return next_date
    
#########################################################################

# Function which takes in one instance of the main data frame
# and returns a subset of this data frame
# including the employees who are retiring in a month
def _FindRetiringEmployees_(main_df, curr_date):
    # we have to make the query to the data frame for the result
    Query = f"DOR == '{curr_date}'"
    new_df = main_df.query(Query)

    return new_df

#########################################################################

# Function to check and return a valid stopping end of month date
def _GiveCorrectStopDate_(first_retirement_date, last_retirement_date, stop_date):
    # correct range we just have to shift the date to the last retirement end of month date
    if stop_date.month == 2:
        if _IsLeapYear_(stop_date.year):    
            # february has 29 days
            if stop_date.day != 29:
                return stop_date - timedelta(stop_date.day)
        else:
            if stop_date.day != 28:
                return stop_date - timedelta(stop_date.day)
    
    if stop_date.month in [1,3,5,7,8,10,12]:
        # months with 31 days
        if stop_date.day != 31:
            return stop_date - timedelta(stop_date.day)
    if stop_date.month in [4,6,9,11]:
        # months with 30 days
        if stop_date.day != 30:
            return stop_date - timedelta(stop_date.day)
    
    # if program reaches here, means the user already input a valid retirement date
    return stop_date

    


