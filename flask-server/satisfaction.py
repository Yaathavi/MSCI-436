import pandas as pd

def cleanSatisfaction():
    xls = pd.ExcelFile('./data/data.xlsx')
    df_sat = pd.read_excel(xls, sheet_name='Satisfaction ')

    return df_sat

def setUtil():
    df1 = cleanSatisfaction()

    weights = {'Excellent': 0.4, 'Good': 0.3, 'Fair': 0.2, 'Poor': 0.1}
    df1['UtilityScore'] = (df1['Excellent'] * weights['Excellent'] +
                      df1['Good'] * weights['Good'] +
                      df1['Fair'] * weights['Fair'] +
                      df1['Poor'] * weights['Poor'])
    
    df1["UtilityScore"] = df1["UtilityScore"].replace(0, df1["UtilityScore"].mean())

    min_util = df1['UtilityScore'].min()
    max_util = df1['UtilityScore'].max()
    df1['Utility_MinMaxScaled'] = (df1['UtilityScore'] - min_util) / (max_util - min_util)
    df1 = df1.reset_index(drop=True)
    return df1

def getSatis():
    df1 = setUtil()
    return df1

# xls = pd.ExcelFile('./data/data.xlsx')
# df_sat = pd.read_excel(xls, sheet_name='Satisfaction ')