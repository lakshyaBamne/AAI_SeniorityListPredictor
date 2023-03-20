# Importing the required libraries
import routines

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datetime import date, timedelta

#########################################################################
# First import the required details from the given input excel file
#########################################################################

inp_file = "input.xlsx"

# all the fields are required by the user in the final excel sheets
# inp_fields = ["EMP_NO", "NAME", "POST", "RANK", "DOB", "DOJ_AAI", "DOR"]

# this is the main Data Frame which has all the information we need
main_df = pd.read_excel(inp_file)

#########################################################################
# Let us create a list of months through which
# we will track the status and rank of the employees
#########################################################################

# for this we need to find the first and the last dates 
# on which some employee retires in the given input list
first_retirement_date = main_df["DOR"].min().date()
last_retirement_date = main_df["DOR"].max().date()

# temp date for first time, just to make iterations happen
stop_date = first_retirement_date - timedelta(1)

# we should get the input from the user specifying 
# till what date does he want the program to run and produce the rank list

print("-------------------------------------------------------------------------------------------------")
print(f"First retirement happens on : {first_retirement_date}")
print(f"Last retirement happens on : {last_retirement_date}")
print("Kindly enter a date in this range only !!")
print("-------------------------------------------------------------------------------------------------")

while True:
    stop_yr, stop_month, stop_day = tuple(map(int, input("Enter your Super Annuation Date (YYYY-MM-DD) : ").split('-')))
    stop_date = date(stop_yr, stop_month, stop_day)

    if stop_date < first_retirement_date or stop_date > last_retirement_date:
        print("-------------------------------------------------------------------------------------------------")
        print(f"[ERROR] : First retirement happens on : {first_retirement_date}")
        print(f"[ERROR] : Last retirement happens on : {last_retirement_date}")
        print("[ERROR] : Kindly enter a date IN this range!!")
        print("-------------------------------------------------------------------------------------------------")
    else:
        break

# we need to give a condition that if stop_date entered by the user
# is after the last retirement_date, then it should return output
# corresponding to the last_retirement_date
stop_date = routines._GiveCorrectStopDate_(first_retirement_date, last_retirement_date, stop_date)

# giving the one month before supernation date retirement list to the user
stop_date = stop_date - timedelta(stop_date.day)

# print(f"Normalised date is : {stop_date}")

# now we can create a list of months and years on which ranks are calculated
months = []

# first we need to append the first month
months.append(first_retirement_date)

some_month = first_retirement_date

while( some_month != stop_date ):
    some_month = routines._NextEndOFMonth_(some_month)
    months.append(some_month)


# print(f"Months = [{months[0]}, {months[1]}, {months[2]}, ... , {months[-3]}, {months[-2]}, {months[-1]}]")


#########################################################################
# first let us initialize the list of dictionaries
#########################################################################

# Structure of the dictionary of dictionaries to store the rank trend of the employees
#   rank_trend = {
#       "EMP_NO_1" : {
#           "INDEX" : <primary key of the user in main data frame>
#           "NAME" : <name of employee>
#           "DOR : <date of retirement of the employee>
#           "MONTHS" : <months from starting till retirement month>
#           "RANKS" : <rank of the employee through the months>
#       },
#       "EMP_NO_1" : {
#           "INDEX" : <primary key of the user in main data frame>
#           "NAME" : <name of employee>
#           "DOR : <date of retirement of the employee>
#           "MONTHS" : <months from starting till retirement month>
#           "RANKS" : <rank of the employee through the months>
#       },
#       .
#       .        
#   }
#   

rank_trend = {}

# Structure of the List given by the iloc/loc function
# [
#   0 => "RANK" : 1,
#   1 => "POST" : 'GM', 
#   3 => "EMP_NO" : 10008900, 
#   4 => "NAME" : 'RAVI KANT', 
#   8 => "DOB" : Timestamp('1963-08-13 00:00:00'), 
#   9 => "DOJ_AAI" : Timestamp('1990-07-03 00:00:00'), 
#   10 => "DOR" : Timestamp('2023-08-31 00:00:00')
# ]

for i in range(len(main_df)):
    # getting a single row from the data frame
    emp = list(main_df.iloc[i])

    rank_trend[f"{emp[3]}"] = {
        "INDEX" : i,       # primary key in main data frame
        "NAME" : emp[4],   # name of employee
        "DOR" : emp[10].date(),  # Date of retirement
        "MONTHS" : [], # Months at which rank is observed
        "RANK" : []        # ranks at instances in the months list
    }

# #########################################################################
# # Now we should start the iterations and update the data frame
# # As well as the dictionary of data trends
# #########################################################################

# dictionary to store the number of employees retired
num_retired = {}

# Iterations stop when all the months have been used
for i in range( len(months) ):
    # in the beginning we should update the ranks with respect to months
    # in the rank trend data frame for the employees who are still in the data frame

    # we need to update the rank for employees who are remaining in the data frame
    for j in list(main_df.index):
        try:
            one_emp = list(main_df.iloc[j])

            rank_trend[f"{one_emp[3]}"]["MONTHS"].append(months[i])
            rank_trend[f"{one_emp[3]}"]["RANK"].append( one_emp[0] )
        except:
            pass

    # printing the rank of employee 10002432 as a reference for testing
    print("---------------------------------------------------------------------------------------")
    test_var_curr_rank = rank_trend["10002432"]["RANK"][-1]
    print(f"Rank of EMP-{10002432} in {months[i]} => { test_var_curr_rank }")
    print("---------------------------------------------------------------------------------------")

    # after this we should find the new set of retiring employees
    # getting the new data frame
    curr_retirement_df = routines._FindRetiringEmployees_( main_df, months[i] )

    print("---------------------------------------------------------------------------------------")
    print(f"Current month : {months[i]}")

    print(f"Retiring employees : { list(curr_retirement_df.index) }")

    # we should first append the length of the data frame
    # i.e. the number of employees retiring in the given month
    num_retired[f"{months[i]}"] = {
        "NUM_RETIRED" : len(curr_retirement_df)
    }

    # now we should update the rank of employees based on the 
    # retiring employees in a given month
    retiring_index = list( curr_retirement_df.index )

    # we update the rank of each row in the data frame
    for j in range(len(main_df)):
        try:
            # we need to count how many employees with a rank lower
            # than the particular employee retired

            # rank of the employee used in the iteration
            emp_rank = int(main_df.loc[j, ["RANK"]])
            
            # store the number of employees above empoloyee retiring
            count = 0

            for k in retiring_index:
                if emp_rank > k:
                    count = count + 1
            
            # update the rank of the employees in the main data frame
            main_df.loc[j, ["RANK"]] = main_df.loc[j, ["RANK"]] - count
        except:
            pass


    # now we need to delete the retiring employees from the main data frame
    main_df = main_df.drop(labels=retiring_index, axis=0)


print("===========================================================")

print(rank_trend["10002432"]["NAME"])
print(rank_trend["10002432"]["MONTHS"])
print(rank_trend["10002432"]["RANK"])

print("===========================================================")

# writing the main_df after execution is complete in an excel file
with pd.ExcelWriter("output.xlsx") as writer:
    main_df.to_excel(writer, f"Ranks at {stop_date}")
