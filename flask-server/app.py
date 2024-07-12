from flask import Flask, request, render_template
from averages import getAvgComp, getAvgEasy
from tuition import saveMoney, spendMoney
from satisfaction import getSatis
from employment import getEmploy
from retention import getRetention
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getRankings", methods=['POST'])
def getUtilEasy():
    # Retrieve data from users survey results
    try:
        program = request.form.get('fieldOfStudy')
        tuition = float(request.form.get('tuition'))
        average = float(request.form.get('average'))
        tuitionCalc = request.form.get('tuitionCalc')
        averageCalc = request.form.get('averageCalc')

        # sample weights
        w_satis = max(1, min(5, float(request.form.get('w_satis'))))
        w_tuition = max(1, min(5, float(request.form.get('w_tuition'))))
        w_average = max(1, min(5, float(request.form.get('w_average'))))
        w_employ = max(1, min(5, float(request.form.get('w_employ'))))
        w_retention = max(1, min(5, float(request.form.get('w_retention'))))
    except (TypeError, ValueError) as e:
        return {"error": "Invalid or missing data"}

    # find utility for averages
    df_avg = pd.DataFrame()
    if averageCalc == "competitive":
        df_avg = getAvgComp(program, average)
    else:
        df_avg = getAvgEasy(program, average)
    print("df_avg:", df_avg)

    # find utility for tuition
    df_tuition = pd.DataFrame()
    if tuitionCalc == "spendMoney":
        df_tuition = spendMoney(tuition, program)
    else:
        df_tuition = saveMoney(tuition, program)
    print("df_tuition:", df_tuition)

    # find utility for satisfaction
    df_satis = pd.DataFrame()
    df_satis = getSatis()
    print("df_satis:", df_satis)

    # find utility for employment
    df_employ = pd.DataFrame()
    df_employ = getEmploy(program)
    print("df_employ:", df_employ)

    # find utility for retention
    df_retention = pd.DataFrame()
    df_retention = getRetention()
    print("df_retention:", df_retention)

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
            return float('nan')  # Return NaN if any value in the row is NaN
        else:
            return row.sum()

    df_combined['TotalUtil'] = df_combined[['W_AvgUtil', 'W_TuitionUtil', 'W_SatisUtil', 'W_EmployUtil', 'W_RetentionUtil']].apply(addUtil, axis=1)

    # sort from high to low utility
    df_combined = df_combined.sort_values(by='TotalUtil', ascending=False)

    # Get the top 3 universities
    top_3_universities = df_combined.head(3)

    # Render the results in the template
    tables = top_3_universities.to_html(classes='data', index=False)
    return render_template("results.html", tables=tables, program=program, tuition=tuition, average=average,
                           w_satis=w_satis, w_tuition=w_tuition, w_average=w_average, w_employ=w_employ, w_retention=w_retention)

if __name__ == "__main__":
    app.run(debug=True)
