#./.venv/Scripts/activate
# python -m venv .venv
# python server.py

from flask import Flask, request
from averages import setUtilEasy
import pandas as pd

app = Flask(__name__)

# Reading the excel files
xls = pd.ExcelFile('./data/data.xlsx')
df_avg = pd.read_excel(xls, sheet_name='Admission Avg')

# set util easy
# df_avg = setUtilEasy(df_avg, "Engineering", 0.854)
# print(df_avg)

# API Routes
@app.route("/members")
def members():
    return {"message": "head"}

@app.route("/getUtilEasy", methods=['GET'])
def getUtilEasy():
    program = request.args.get('program')

    if program is None:
        return {"error": "Missing input_string or input_number"}
    else:
        return {"program": program}

    # df_avg = setUtilEasy(df_avg, "Engineering", 0.854)
    print("hi")
    return {"program": program}



if __name__ == "__main__":
    app.run(debug=True)
