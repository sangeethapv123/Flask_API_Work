from flask import Flask,request
from models import Student
from flask_restx import Api,Resource

app = Flask(__name__);
api = Api(app);

class Details(Resource):

    try:
        Student.create_table();

    except Exception as e:
        print(e);

    def get(self,name):


     try:

         employee_details = {}

         details = Student.get_data(name);

         for i in details:
            employee_details['id']   = i[0];
            employee_details['name'] = i[1];

         return  employee_details,200

     except Exception as e:

         print(e);


    def delete(self,name):

        Student.delete_data(name);
        return {"Status":"Record Removed"},200


    def post(self,name):

     try:

        data       = request.get_json();
        id_list    = (data['id'])
        name_list  = data['name'];
        my_tup     = list(zip(id_list,name_list))
        print(my_tup)
        z = Student.insert_data(my_tup);


        return {"Status":"Data_Inserted","data":z},201

     except Exception as e:
         print(e);

api.add_resource(Details,'/student/<string:name>')
app.run(debug=True);
