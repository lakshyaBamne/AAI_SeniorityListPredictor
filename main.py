# Importing the required libraries and packages
import pandas as pd
import helper
import matplotlib.pyplot as plt
import numpy as np

####################################################################################
# MAIN PROGRAM STARTS 
####################################################################################

# importing the excel file in a dataframe
df = pd.read_excel('DPC_SeniorityList.xlsx', usecols = ["RANK", "POST", "Emp No", "Name", "DOB", "DOJ AAI", "DOR"])

first_year = int(df['DOR'].min().date().year)
last_year = int(df['DOR'].max().date().year)

len(df[(df['DOR'] > '2023-1-1') & (df['DOR'] <= '2023-12-31')])

# let us store the number of employees retiring in a list
yearly_retirements = []

for one_year in range(first_year, last_year+1):
    yearly_retirements.append(len(df[(df['DOR'] > f'{one_year}-1-1') & (df['DOR'] <= f'{one_year}-12-31')])
)

# initial month and year should be the earliest retirement date of some employee
min_date = df['DOR'].min()

curr_month = min_date.date().month
curr_year = min_date.date().year

# curr_month = helper._FindCurrMonthYear_()[0]
# curr_year = helper._FindCurrMonthYear_()[1]

# now we will need the number of employees in the data frame
num_employee = len(df)

# df_new = helper._FindRetiringEmployees_(df,curr_month, curr_year)[0]

# we should store the number of employees retiring in any month, year
# in another data frame with three columns => month, year, num_retired
df_num_retired_emp = pd.DataFrame({
    'month' : pd.Series(dtype='int'),
    'year' : pd.Series(dtype='int'),
    'num_retired' : pd.Series(dtype='int')
})

# we also create a data frame that stores the rank of each employee across months
# initially there are only 3 fields but more are added in the iterations
df_rank_trend = pd.DataFrame({
    'emp_no' : df['Emp No'],
    'name' : df['Name'],
    'DOR' : df['DOR'],
    'initial_rank' : df['RANK']
})

# we should create the excel workbook "RetiredIn.xlsx" so that sheets can be appended to it
testDf = pd.DataFrame(list())

# writing empty DataFrame to the excel file to which sheets would be appended
testDf.to_excel('RetiredIn.xlsx')

count_emp_retired = 0

# Observe that some employees may have retired before the month the
# program starts, hence the data frame may not be empty to stop the loop

# our process will go on till the data frame is exhausted
while len(df) > 0:
    # new data frame to store the employees retiring in the current month and year
    df_new = helper._FindRetiringEmployees_(df,curr_month, curr_year)[0]

    # we need to add the length of this new data frame to the 
    # data frame which represents the number of employees retired in a month,year
    df_num_retired_emp.loc[len(df_num_retired_emp)] = [curr_month, curr_year, len(df_new)]

    # list containing the indexes of employees which are retiring in the current month
    retiring_index_list = helper._FindRetiringEmployees_(df,curr_month, curr_year)[1]

    if len(retiring_index_list) > 0:
        print(f"...[LOG]... Added {len(df_new)} retired employees in {curr_month}, {curr_year}")

        count_emp_retired = count_emp_retired + len(retiring_index_list)

        # now we need to export this new data frame as an excel sheet
        # these files should be exported in the excel workbook => "RetiredIn.xlsx"
        # name of the sheet would be => "RetiredIn_<curr_month>_<curr_year>"
        wb_name = "RetiredIn.xlsx"
        sheet_name = "RetiredIn_" + str(curr_month) + "_" + str(curr_year)

        # exporting the data frame to excel sheet in the output workbook
        helper._ExportDFtoExcel_(df_new, wb_name, sheet_name)

        # now we need to update the rank of employees who are not retiring
        # this includes the updation of rank after each month for employees not retiring
        # then deleting the employees who are retiring
        df = helper._UpdateRankList_(df, curr_month, curr_year, df_rank_trend)

    # now we should update the month and the year for the loop to proceed
    curr_month, curr_year = helper._UpdateMonthYear_(curr_month, curr_year)

# now we export the data frames made to show analysis about rank of employees
# helper._ExportDFtoExcel_(df_rank_trend, "EmployeeRankTrend", "Sheet 1")

with pd.ExcelWriter('MonthlyRetirements.xlsx') as writer:
    df_num_retired_emp.to_excel(writer, 'Sheet 1')

# let us plot the trend of retirements made in a particular year
# for this we need to use the df_num_retired_emp data frame


# giving the rank trend file as output
with pd.ExcelWriter('EmployeeRankTrend.xlsx') as writer:
    df_rank_trend.to_excel(writer, 'Sheet 1')


# Plotting the trend showing the number of retirements through the years
fig = plt.figure(figsize=(10,10))

years = []

for i in range(first_year, last_year+1):
    years.append(i)

# x_axis = np.linspace(min(yearly_retirements), max(yearly_retirements), num=len(yearly_retirements),endpoint=True)

plt.bar(years,yearly_retirements, label='Yearly Retirements', color='green', width=0.1)

plt.legend()

plt.show()


# we can add the system where an employee enters their employee number
# and is shown the trend of his rank progression throughout the years

# the query returns the initial rank (at the making of the list) and then
# only the rank of the employee at the end of the proceeding year is taken

# first we get the employment number of the employee
emp_num = int(input("Enter the Employment Number : "))

# now we should get the entire row for this employee
emp_row = df_rank_trend.loc[ df_rank_trend['emp_no'] == emp_num ]

# now we need the index of this row to get the required list
emp_index = emp_row.index

temp_df = df_rank_trend.loc[emp_index]



# removing the columns where value of rank is missing
# because for every employee, after some year they will retire
temp_df = temp_df.dropna(how='all', axis=1)


first_rank_column = 3
final_rank_column = temp_df.shape[1]-1

# # we need to know the first and last year of the ranking of the employee
# final_year = 

# now we should extract the values of all columns after the index
temp_df = temp_df.iloc[:, first_rank_column:final_rank_column]

# now we can transpose this data frame for more efficiency
temp_df = temp_df.T



# imp imp imp
# we can get the index with a specific year using this
# test_df = temp_df[['2024' in s for s in temp_df.index]]
# print(test_df)

# we can start with the initial year and go one by one
# till the query returns no rows for some year
initial_year = int(helper._FindCurrMonthYear_()[1])

# lists to store the year and the rank at that year to be plotted
x_vals = []
y_vals = []

test_df = temp_df[[f'{initial_year}' in s for s in temp_df.index]]


while( len(test_df) > 0 ):
    # first we should append the initial year to the list
    x_vals.append(initial_year)
    
    initial_year = initial_year + 1

    # append the y_values
    y_vals.append( int(test_df.iloc[ len(test_df)-1 ]) )

    # we shold now extract the df with indices having the year in them
    test_df = temp_df[[f'{initial_year}' in s for s in temp_df.index]]

# we should make some changes to y_values for correct visualization
for i in range(len(y_vals)):
    # first we make every value it's negative
    y_vals[i] = y_vals[i] * (-1)

# now we find the lowest value in the y_vals list

min_val = min(y_vals)

for i in range(len(y_vals)):
    y_vals[i] = y_vals[i] + ( (-1)*min_val )

# now we can plot these values for the given employee
fig2 = plt.figure(figsize=(10,10))

plt.plot(x_vals, y_vals, label=f"Rank Trend for {emp_num}")

plt.legend()

plt.show()




