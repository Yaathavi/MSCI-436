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
    if averageCalc == "competitive":
        df_avg = getAvgComp(program, average)
    else:
        df_avg = getAvgEasy(program, average)

    # find utility for tuition
    if tuitionCalc == "spendMoney":
        df_tuition = spendMoney(tuition, program)
    else:
        df_tuition = saveMoney(tuition, program)

    # find utility for satisfaction
    df_satis = getSatis()

    # find utility for employment
    df_employ = getEmploy(program)

    # find utility for retention
    df_retention = getRetention()

    # combine the utilities from each df
    df_combined = pd.DataFrame()
    df_combined["University"] = df_avg["University"]
    df_combined["AvgUtil"] = df_avg["Utility_MinMaxScaled"] * w_average
    df_combined["TuitionUtil"] = df_tuition["Utility_MinMaxScaled"] * w_tuition 
    df_combined["SatisUtil"] = df_satis["Utility_MinMaxScaled"] * w_satis
    df_combined["EmployUtil"] = df_employ["Utility_MinMaxScaled"]  * w_employ 
    df_combined["RetentionUtil"] = df_retention["Utility_MinMaxScaled"] * w_retention

    # add the utility by school
    def addUtil(row):
        if row.isnull().any():
            return None
        else:
            return row.sum()
    df_combined['TotalUtil'] = df_combined[['AvgUtil', 'TuitionUtil', 'SatisUtil', 'EmployUtil', 'RetentionUtil']].apply(addUtil, axis=1)

    # apply the weights
    # df_combined['TotalUtil'] = (df_combined["AvgUtil"] +
    #                             df_combined["TuitionUtil"]+
    #                             df_combined["SatisUtil"] +
    #                             df_combined["EmployUtil"]+
    #                             df_combined["RetentionUtil"])

    # sort from high to low utility
    df_combined = df_combined.sort_values(by='TotalUtil', ascending=False)
    print(df_combined)

    # Get the top 5 universities
    top_5_universities = df_combined.head(5)
    df_cleaned = top_5_universities.dropna(subset=['TotalUtil'])
    # df_cleaned = top_5_universities

    # Render the results in the template
    tables = df_cleaned.to_html(classes='data', index=False)
    return render_template("results.html", tables=tables, program=program, tuition=tuition, average=average,
                           w_satis=w_satis, w_tuition=w_tuition, w_average=w_average, w_employ=w_employ, w_retention=w_retention)

if __name__ == "__main__":
    app.run(debug=True)
