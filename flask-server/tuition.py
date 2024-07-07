import pandas as pd

def cleanTuition(df):
    df1 = pd.DataFrame()
    df1["University"] = df["University"]
    df1["Program"] = df["Program"]
    df1["Tuition"] = df["Total Fees"]
    return df1

# set the program to the one they are looking for
def setProgram(df, program):
    df_filtered = df
    df_filtered = df[(df['Program'] == program) & (~df['Tuition'].isna())]
    return df_filtered

# rather save money
def saveMoney(df, tuition, program):
    df1 = df
    df1 = cleanTuition(df1)
    df1 = setProgram(df1, program)

    # Find the difference 
    df1["Tuition_Diff"] = df1["Tuition"] - tuition

    min_diff = df1['Tuition_Diff'].min()
    max_diff = df1['Tuition_Diff'].max()
    df1['Utility_MinMaxScaled'] = 1 - ((df1['Tuition_Diff'] - min_diff) / (max_diff - min_diff))
    return df1

# don't mind spending more as long as its not higher than your budget
def spendMoney(df, tuition, program):
    df1 = df
    df1 = cleanTuition(df1)
    df1 = setProgram(df1, program)

    # Find the difference 
    df1["Tuition_Diff"] = df1["Tuition"] - tuition

    # Set the utility - decrease as it increases past your budget
    df1['Utility'] = df1['Tuition_Diff'].apply(lambda x: x if x > 0 else 0)

    min_diff = df1['Utility'].min()
    max_diff = df1['Utility'].max()
    df1['Utility_MinMaxScaled'] = 1 - ((df1['Utility'] - min_diff) / (max_diff - min_diff))
    return df1

### Testing
# xls = pd.ExcelFile('./data/data.xlsx')
# df_tuition = pd.read_excel(xls, sheet_name='Tuition Cost')

# df_util = spendMoney(df_tuition, 7500, "Arts and Science")
# print(df_util)
