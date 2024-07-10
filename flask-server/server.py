#./.venv/Scripts/activate
# python -m venv .venv
# python server.py

from flask import Flask, request
from averages import getAvgComp, getAvgEasy
from tuition import saveMoney, spendMoney
from satisfaction import getSatis
from employment import getEmploy
from retention import getRetention
import pandas as pd

app = Flask(__name__)

# set util easy
# df_avg = setUtilEasy(df_avg, "Engineering", 0.854)
# print(df_avg)

# API Routes
@app.route("/members")
def members():
    return {"message": "head"}

@app.route("/getRankings", methods=['GET'])
def getUtilEasy():
    # Retrieve data from users survey results
    program = request.args.get('program')
    tuition = request.args.get('tuition')
    average = request.args.get('average')
    tuitionCalc = request.args.get('tuitionCalc')
    averageCalc = request.args.get('averageCalc')

    # sample weights
    w_satis = request.args.get('w_satis')
    w_tuition = request.args.get('w_tuition')
    w_average = request.args.get('w_average')
    w_employ = request.args.get('w_employ')
    w_retention = request.args.get('w_retention')

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

    # turn it into json
    json_result = df_combined[['University', "W_AvgUtil", "W_TuitionUtil", "W_SatisUtil", "W_EmployUtil", "W_RetentionUtil", 'TotalUtil']].to_json(orient='records')
    
    ## YAATHAVI expand on this to account for errors
    if program is None or tuition is None or average is None or tuitionCalc is None or avgCalc is None:
        return {"error": "Missing data"}
    else:
        return {"results": json_result}

if __name__ == "__main__":
    app.run(debug=True)
