from averages import getAvgComp, getAvgEasy
from tuition import saveMoney, spendMoney
from satisfaction import getSatis
from employment import getEmploy
from retention import getRetention
import pandas as pd

# sample data
program = "Kinesiology/Recreation/Physical Education"
tuition = 1500
average = 95
tuitionCalc = "spendMoney"
averageCalc = "competitive"

# sample weights
w_satis = 2
w_tuition = 1
w_average = 4
w_employ = 4
w_retention = 2

# find utility for averages
df_avg = pd.DataFrame()
if averageCalc == "competitive":
    df_avg = getAvgComp(program, average)
else:
    df_avg = getAvgEasy(program, average)


# find utiility for tuition
df_tuition = pd.DataFrame()
if tuitionCalc == "spendMoney":
    df_tuition = spendMoney(tuition, program)
else:
    df_tuition = saveMoney(tuition, program)

# find utility for satisfaction
df_satis = pd.DataFrame()
df_satis = getSatis()

# find utility for employment
df_employ = pd.DataFrame()
df_employ = getEmploy(program)

# find utility for retention
df_retention = pd.DataFrame()
df_retention = getRetention()

# combine the utilities from each df
df_combined = pd.DataFrame()
df_combined["University"] = df_avg["University"]
df_combined["AvgUtil"] = df_avg["Utility_MinMaxScaled"]
df_combined["TuitionUtil"] = df_tuition["Utility_MinMaxScaled"]
df_combined["SatisUtil"] = df_satis["Utility_MinMaxScaled"]
df_combined["EmployUtil"] = df_employ["Utility_MinMaxScaled"]
df_combined["RetentionUtil"] = df_retention["Utility_MinMaxScaled"]

# apply the weights
df_combined['W_AvgUtil'] = df_combined["AvgUtil"] * w_average
df_combined['W_TuitionUtil'] = df_combined["TuitionUtil"] * w_tuition
df_combined['W_SatisUtil'] = df_combined["SatisUtil"] * w_satis
df_combined['W_EmployUtil'] = df_combined["EmployUtil"] * w_employ
df_combined['W_RetentionUtil'] = df_combined["RetentionUtil"] * w_retention

# add the utility by school
def addUtil(row):
    if row.isnull().any():
        return None
    else:
        return row.sum()
    
df_combined['TotalUtil'] = df_combined[['W_AvgUtil', 'W_TuitionUtil', 'W_SatisUtil', 'W_EmployUtil', 'W_RetentionUtil']].apply(addUtil, axis=1)

# sort from high to low utility
df_combined = df_combined.sort_values(by='TotalUtil', ascending=False)
# print(df_combined)

# turn it into json
json_result = df_combined[['University', "W_AvgUtil", "W_TuitionUtil", "W_SatisUtil", "W_EmployUtil", "W_RetentionUtil", 'TotalUtil']].to_json(orient='records')
# print(json_result)


# data cleaning
columns_to_keep = ['University','W_AvgUtil', 'W_TuitionUtil', 'W_SatisUtil', 'W_EmployUtil', 'W_RetentionUtil', 'TotalUtil']
df_data = df_combined[columns_to_keep].copy()
print(df_data)