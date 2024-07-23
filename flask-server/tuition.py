import pandas as pd

def cleanTuition():
    xls = pd.ExcelFile('./data/data.xlsx')
    df = pd.read_excel(xls, sheet_name='Tuition Cost')
    df1 = pd.DataFrame()

    df1["University"] = df["University"]
    df1["Program"] = df["Program"]
    df1["Tuition"] = df["Total Fees"]
    return df1

# set the program to the one they are looking for
def setProgram(df, program):
    df_filtered = df
    # df_filtered = df[(df['Program'] == program) & (~df['Tuition'].isna())]
    df_filtered = df[(df['Program'] == program)]
    return df_filtered

# rather save money
def saveMoney(tuition, program):
    df1 = cleanTuition()
    df1 = setProgram(df1, program)

    # Find the difference 
    df1["Tuition_Diff"] = df1["Tuition"] - tuition

    min_diff = df1['Tuition_Diff'].min()
    max_diff = df1['Tuition_Diff'].max()
    df1['Utility_MinMaxScaled'] = 1 - ((df1['Tuition_Diff'] - min_diff) / (max_diff - min_diff))
    df1 = df1.reset_index(drop=True)
    return df1

# don't mind spending more as long as its not higher than your budget
def spendMoney(tuition, program):
    df1 = cleanTuition()
    df1 = setProgram(df1, program)

    # Find the difference 
    df1["Tuition_Diff"] = df1["Tuition"] - tuition

    # Set the utility - decrease as it increases past your budget
    df1['Utility'] = df1['Tuition_Diff'].apply(lambda x: x if pd.isnull(x) or x > 0 else 1)

    min_diff = df1['Utility'].min()
    max_diff = df1['Utility'].max()
    if min_diff != max_diff:
        df1['Utility_MinMaxScaled'] = 1 - ((df1['Utility'] - min_diff) / (max_diff - min_diff))
    else:
        df1['Utility_MinMaxScaled'] = df1["Utility"]
    df1 = df1.reset_index(drop=True)
    return df1

### Testing
# df_util = saveMoney(13000, "Engineering")
# print(df_util)
