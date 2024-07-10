import pandas as pd

# Clean the averages dataframe
def cleanRetention():
    # Reading the excel files
    xls = pd.ExcelFile('./data/data.xlsx')
    df = pd.read_excel(xls, sheet_name='Retention Rates')

    df1 = df.dropna(axis=1, how='all')
    return df1

# get utility
def scale(df):
    min_retention = df['Retention Rate'].min()
    max_retention = df['Retention Rate'].max()
    df1 = df
    df1['Utility_MinMaxScaled'] = (df1['Retention Rate'] - min_retention) / (max_retention - min_retention)
    return df1

def getRetention():
    df1 = cleanRetention()
    df1 = scale(df1)
    df1 = df1.reset_index(drop=True)
    return df1
