from datetime import date

import pandas as pd

####################################################################################
# FUNCTION DEFINITIONS
####################################################################################

# Function to find the Current Month and year when the function is called
# returns a tuple => (month, year)
def _FindCurrMonthYear_():
    curr_month = date.today().month
    curr_year = date.today().year
    return ( curr_month , curr_year )

# function to check if the given year is a leap year
def _CheckLeapYear_(year):
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

# Function returns a new data frame 
# which contains the data about the employees retiring in the current month
def _FindRetiringEmployees_(curr_df, curr_month, curr_year):
    # first we need to check if the current year is leap year or not
    is_leap_yr = _CheckLeapYear_(curr_year)
    
    # the last date of the month is determined by the month
    # and whether the year is a leap year or not
    if curr_month in [1,3,5,7,8,10,12]:
        end_date = 31
    elif curr_month in [4,6,9,11]:
        end_date = 30
    elif curr_month in [2]:
        if is_leap_yr == 0:
            end_date = 28
        else:
            end_date = 29

    Query = "DOR == '" + str(curr_year) + "-" + str(curr_month) + "-" + str(end_date) + "'"

    # the query made will return the required data frame
    new_df = curr_df.query(Query)

    # we also return a list of index for the employees in this data frame
    retiring_emp_list = list(new_df.index)

    # tuple which has first element as the new data frame
    # and second element as the list of index for retiring employees
    return (new_df, retiring_emp_list)

# Function to update the rank of employees based on the list of
# employees that would retire at the end of month
# function only updates the rank of the employees who are not retiring
# because the employees who would retire in the current month are at their best rank
# after updating the rank of the employees
# function deletes the retiring employees from the original data frame
def _UpdateRankList_(curr_df, curr_month, curr_year, df_rank_trend):
    # first we need to get the list of indices which are of the 
    # employees who are retiring in the current month, year
    retiring_emp_tuple = _FindRetiringEmployees_(curr_df, curr_month, curr_year)

    index_list = retiring_emp_tuple[1]

    row_count = len(curr_df)

    # we should only update the ranks if there is someone retiring in the month
    if len(index_list) > 0:
        for i in range(row_count):
            # if the index is of an employee not retiring
            # then only the employee's rank is updated
            if i not in index_list:
                try:
                    # getting the rank of employee in the data base who is not retiring
                    rank_person = int(curr_df.loc[ i , ["RANK"] ])

                    count = 0
                    for j in index_list:
                        if rank_person > j:
                            count = count + 1
                    curr_df.loc[ i , ["RANK"] ] = curr_df.loc[ i , ["RANK"] ] - count
                except:
                    pass
        # now we need to delete the retiring employees from the main data frame
        curr_df = curr_df.drop(labels=index_list, axis=0)

        # we should add a new field to contain the ranks of employees not retired
        for i in list(curr_df.index):
            df_rank_trend.loc[i, [f'RankIn_{curr_month}_{curr_year}']] = [ curr_df.loc[i]["RANK"] ]

    return curr_df

# Function to export a data frame to an excel file
def _ExportDFtoExcel_(df, wb_name, sheet_name):
    with pd.ExcelWriter( str(wb_name) , mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name)

# Function to update the month and year after the rank list has been updated
def _UpdateMonthYear_(curr_month, curr_year):
    next_month = curr_month
    next_year = curr_year
    if next_month < 12:
        next_month = next_month + 1
    elif next_month == 12:
        next_month = 1
        next_year = next_year + 1

    return (next_month, next_year)


# Function to find the rank of an employee throughout the years
def _GetRankProgress_(df_rank_trend, emp_num):
    pass

