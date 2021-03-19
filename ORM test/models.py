from db import db
import pandas as pd
from marshmallow import Schema
import json
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class school(ma.Schema):

    class Meta:
     fields = ('School_Name','Attendance')

class School_data(db.Model):

    __tablename__ = "school_attendance"
    id = db.Column(db.Integer, primary_key=True);
    School_Name = db.Column(db.String(200));
    Cluster     = db.Column(db.String(200));
    Block       = db.Column(db.String(200));
    District    = db.Column(db.String(200));
    Date         = db.Column(db.DateTime);
    Attendance  = db.Column(db.Integer);

    def __init__(self,id,name,cluster,block,district,date,attendance):
        self.id          =id;
        self.School_Name = name;
        self.Cluster     = cluster;
        self.Block       = block;
        self.District    = district;
        self.Date        = date;
        self.Attendance  = attendance;

    def save_to_db(self):
        db.session.add(self);
        db.session.commit();

    @classmethod
    def get_attendance(cls):
        #this is selct * from sql query
        required_data = cls.query.all();
        obj = school(many=True)
        w = obj.dump(required_data);
        df_pandas = pd.DataFrame(w);
        df_agg = df_pandas.groupby('School_Name')['Attendance'].sum().reset_index();
        print(df_agg)
        return (json.loads(df_agg.to_json(orient='records')))


