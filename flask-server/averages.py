import pandas as pd

# Clean the averages dataframe
def cleanAvg():
    # Reading the excel files
    xls = pd.ExcelFile('./data/data.xlsx')
    df = pd.read_excel(xls, sheet_name='Admission Avg')

    df1 = df.dropna(axis=1, how='all')
    # df1 = df1.drop(columns=['Unnamed: 4', "Unnamed: 8"])
    return df1

# Gets the averages for a program - removes schools without that program
def setAvgs(df, program):
    # df_filtered = df[(df['Program'] == program) & (~df['Overall Average'].isna())]
    df_filtered = df[(df['Program'] == program)]
    return df_filtered

# Create the difference column
def setDiff(df, avg):
    df1 = df
    df1['Difference'] = avg - df['Overall Average']
    return df1

def initAvg(program, avg):
    df1 = cleanAvg()
    df1 = setAvgs(df1, program)
    df1 = setDiff(df1, avg)
    return df1

def scale(df):
    min_utility = df['Utility'].min()
    max_utility = df['Utility'].max()
    df1 = df
    df1['Utility_MinMaxScaled'] = (df1['Utility'] - min_utility) / (max_utility - min_utility)
    return df1

# Sets the utility if they want the highest chance of getting into a program
def getAvgEasy(program, avg):
    # Clean the dataframe
    df1 = initAvg(program, (avg/100))

    # Calculates the utility for each row 
    def calcUtil(diff):
        return 1 + diff
    
    df1['Utility'] = df1['Difference'].apply(lambda x: calcUtil(x))
    df1 = scale(df1)
    df1 = df1.reset_index(drop=True)
    return df1

# Sets the utility if they want to get into the most competitive program
def getAvgComp(program, avg):
    # Clean the dataframe
    df1 = initAvg(program, (avg/100))

    # Create a function that will calculate the utility
    # If it deviates from the person's average, the utility decreases - they will get recommended a program closest to their average
    def calcUtil(diff):
        return 1 - abs(diff) 
        
    df1['Utility'] = df1['Difference'].apply(lambda x: calcUtil(x))
    df1 = scale(df1)
    df1 = df1.reset_index(drop=True)
    return df1


# # TESTING ***************
#print(getAvgComp("Engineering", 75))


