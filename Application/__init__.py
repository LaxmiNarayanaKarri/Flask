from flask import Flask,render_template,url_for,request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Resource,Api,abort,fields,marshal_with
import json
import jwt
from flask import jsonify
from flask_session import Session
from flask_bcrypt import Bcrypt

from functools import wraps
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SECRET_KEY'] = 'e7d274119f42ba9c69b123e2'
app.config['SESSION_TYPE'] = 'filesystem'
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)
login_manager.login_view="login"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
login_manager.login_message_category="info"
app.config["JWT_TOKEN_LOCATION"] = ["headers","query_string"]

from Application import route
from Application.models import Employee

#API
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
         # Return the user information attached to the token
        return f(*args, **kwargs)
    return decorator


class Search_all(Resource):
    @token_required
    def get(self):
        employees = Employee.query.all()
        list_of_emplpoyees={}
        for employee in employees:
            list_of_emplpoyees[employee.id]={
                "id" : employee.id,
                "First_Name" :employee.First_Name,
                "Last_Name":employee.Last_Name,
                "Email" :employee.Email,
                "PhoneNumber" :employee.PhoneNumber,
                "DOB": json.dumps(employee.DOB , default=str)[1:-1],
                "Address" :employee.Address,
            }
        return list_of_emplpoyees

class Search(Resource):
    @token_required
    def get(self,first_name,address):
        employees = Employee.query.filter_by(Address=address, First_Name=first_name).all()
        list_of_emplpoyees={}
        for employee in employees:
            list_of_emplpoyees[employee.id]={
                "id" : employee.id,
                "First_Name" :employee.First_Name,
                "Last_Name":employee.Last_Name,
                "Email" :employee.Email,
                "PhoneNumber" :employee.PhoneNumber,
                "DOB": json.dumps(employee.DOB , default=str)[1:-1],
                "Address" :employee.Address,
            }
        return list_of_emplpoyees

api.add_resource(Search,'/search/<string:first_name>/<string:address>')
api.add_resource(Search_all,'/search')






