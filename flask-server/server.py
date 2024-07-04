#./.venv/Scripts/activate
# python -m venv .venv
# python server.py

from flask import Flask
from testing import getAvgs, cleanAvg
import pandas as pd

app = Flask(__name__)

# Reading the excel files
xls = pd.ExcelFile('./data/data.xlsx')
df_avg = pd.read_excel(xls, sheet_name='Admission Avg')

# Cleaning the excel files
df_avg = cleanAvg(df_avg)

# Members API Route
@app.route("/members")
def members():
    return {"message": "head"}

if __name__ == "__main__":
    app.run(debug=True)
