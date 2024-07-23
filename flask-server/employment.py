import pandas as pd

# Clean the averages dataframe
def cleanEmploy():
    # Reading the excel files
    xls = pd.ExcelFile('./data/data.xlsx')
    df = pd.read_excel(xls, sheet_name='Employment Rates')

    df1 = df.dropna(axis=1, how='all')
    return df1

# removes schools without that program
def setEmploy(df, program):
    df_filtered = df[(df['Program'] == program)]
    return df_filtered

def scale(df):
    min_employ = df['Employment Rate'].min()
    max_employ = df['Employment Rate'].max()
    df1 = df
    df1['Utility_MinMaxScaled'] = (df1['Employment Rate'] - min_employ) / (max_employ - min_employ)
    return df1

def getEmploy(program):
    df1 = cleanEmploy()
    df1 = setEmploy(df1, program)
    df1 = scale(df1)
    df1 = df1.reset_index(drop=True)
    return df1

# print(getEmploy("Kinesiology"))