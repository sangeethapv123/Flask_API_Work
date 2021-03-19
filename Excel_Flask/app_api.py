from werkzeug import exceptions
import json
from flask import Flask,request
from flask_restx import Api,Resource
import pandas as pd

app = Flask(__name__);
api = Api(app);

class School(Resource):

    @classmethod
    def get(cls):
        df_pandas = pd.read_excel("D:\PDS\PDS API\Files\student_attendance_outlier.xls");
        df_aggr = df_pandas.groupby("District") ["School Name"].count().reset_index();
        return json.loads(df_aggr.to_json(orient='records'));

class Attendance(Resource):

    @classmethod
    def get(cls):
        df_pandas = pd.read_excel("D:\PDS\PDS API\Files\student_attendance_outlier.xls");
        df_aggr = df_pandas.groupby("School Name") ["Attendance"].sum().reset_index();
        return json.loads(df_aggr.to_json(orient='records'));

api.add_resource(School,"/school/")
api.add_resource(Attendance,"/attendance/")
app.run(debug=True);


