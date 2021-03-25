from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
from models import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
api = Api(app);

app.config['SECRET_KEY'] = 'thisissecret'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:tibil4127@localhost/userdb"

@app.before_first_request
def create_tables():
    db.create_all()

def token_required(f):
    @wraps(f)
    def decorated(*args ,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(({'message' : 'Token is missing!'}))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
            print(current_user.admin)
            print(current_user.name)
        except :
            return jsonify({'message':'Token is invalid!'})
        return f(current_user=current_user, *args, **kwargs)
    return decorated


class Users(Resource):
    @token_required
    def get(self,current_user):
        print( (current_user.admin))
        if not current_user.admin:
            return jsonify({'message': 'Cant perform this function!'})
        users = User.query.all()
        output = []

        for user in users:
            user_data = {}
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)
        return jsonify({'users' : output})

    @token_required
    def post(self,current_user):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform this function!'})
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'],method='sha256')
        new_user = User(name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'})


class User_data(Resource):
    @token_required
    def get(self,current_user,user_id):
        if not current_user.admin:
            return jsonify({'message': 'Cant perform this function!'})
        user = User.query.filter_by(id = user_id).first()
        if not user:
            return jsonify({'message' : 'No user found!'})
        user_data = {}
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        return jsonify(({'user' : user_data}))

    @token_required
    def put(self,current_user,user_id):
        if not current_user.admin:
            return jsonify({'message': 'Cant perform this function!'})
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'No user found!'})
        user.admin = True
        db.session.commit()
        return jsonify(({'message' : 'User has been changed to admin!'}))

    @token_required
    def delete(self,current_user,user_id):
        if not current_user.admin:
            return jsonify({'message': 'Cant perform this function!'})
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'No user found!'})

        db.session.delete(user)
        db.session.commit()
        return jsonify(({'message' : ' The user has been deleted!'}))

class Login(Resource):

    def get(self):
        auth = request.authorization
        if not auth.username and not auth.password:
            return make_response('Could not verify, please provide the username and password')
        user = User.query.filter_by(name=auth.username).first()
        if not user:
            return make_response('User not found!')

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({"token": token.decode('UTF-8')})
        if not auth.password:
            return make_response('Could not verify, please provide the password')
        if (user.password != auth.password):
            return make_response('Password is incorrect!')

db.init_app(app)
api.add_resource(Users,'/user');
api.add_resource(User_data,'/user/<user_id>');
api.add_resource(Login,'/login');
app.run();