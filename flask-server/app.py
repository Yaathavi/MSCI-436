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
    df_combined["AvgUtil"] = df_avg["Utility_MinMaxScaled"]
    df_combined["TuitionUtil"] = df_tuition["Utility_MinMaxScaled"]
    df_combined["SatisUtil"] = df_satis["Utility_MinMaxScaled"]
    df_combined["EmployUtil"] = df_employ["Utility_MinMaxScaled"]
    df_combined["RetentionUtil"] = df_retention["Utility_MinMaxScaled"]

    # apply the weights
    df_combined['TotalUtil'] = (df_combined["AvgUtil"] * w_average +
                                df_combined["TuitionUtil"] * w_tuition +
                                df_combined["SatisUtil"] * w_satis +
                                df_combined["EmployUtil"] * w_employ +
                                df_combined["RetentionUtil"] * w_retention)

    # sort from high to low utility
    df_combined = df_combined.sort_values(by='TotalUtil', ascending=False)

    # Get the top 5 universities
    top_5_universities = df_combined.head(5)

    # Render the results in the template
    tables = top_5_universities.to_html(classes='data', index=False)
    return render_template("results.html", tables=tables, program=program, tuition=tuition, average=average,
                           w_satis=w_satis, w_tuition=w_tuition, w_average=w_average, w_employ=w_employ, w_retention=w_retention)

if __name__ == "__main__":
    app.run(debug=True)
