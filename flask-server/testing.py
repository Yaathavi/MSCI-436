import pandas as pd

# xls = pd.ExcelFile('./data/data.xlsx')
# Read each sheet into a DataFrame
# df1 = pd.read_excel(xls, sheet_name='Admission Avg')
# # Get rid of columns with NaN values
# df1 = df1.dropna(axis=1, how='all')
# df1 = df1.drop(columns=['Unnamed: 4', "Unnamed: 8"])

# Clean the averages dataframe
def cleanAvg(df):
    df1 = df.dropna(axis=1, how='all')
    df1 = df.drop(columns=['Unnamed: 4', "Unnamed: 8"])
    return df1

# Gets the averages for a program - removes schools without that program
def getAvgs(program, df):

    df_filtered = df[(df['Program'] == program) & (~df['Overall Average'].isna())]
    return df_filtered

# print(getAvgs("Engineering").head())
# head = df1.head()
# print(head)