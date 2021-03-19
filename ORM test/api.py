from flask import Flask
from flask_restx import Api,Resource
from models import  School_data
from db import db
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database,database_exists
import csv

app = Flask(__name__);
api = Api(app);
engine = create_engine("postgres://postgres:tibil4127@localhost/school_db");
if not database_exists(engine.url):
    create_database(engine.url);
else:
    pass;
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:tibil4127@localhost/school_db"

@app.before_first_request
def create_tables():
    db.create_all()

class ETL(Resource):

    def post(self):

      with open("D:/PDS/PDS API/Files/student_attendance_outlier.csv","r") as f:

        row = csv.reader(f);
        next(row,None);
        for rows in row:
            if len(rows)>0:
                print(rows)
                record = School_data(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6]);
                School_data.save_to_db(record);

class Attendance(Resource):

    def get(self):

        data = School_data.get_attendance();
        return data,200

db.init_app(app)
api.add_resource(ETL,'/insert_data');
api.add_resource(Attendance,'/get_attendance/')
app.run();
