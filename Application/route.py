from Application import app
from flask import render_template,redirect,url_for,flash,session,request
from Application.forms import RegistrationForm,LoginForm,SearchForm
from Application.models import Employee
from Application import db
from flask_login import login_user,logout_user,login_required,current_user
import requests
import json
import jsonify
import datetime
import requests
from Application import jwt


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if check_Admin_Available():
        form = RegistrationForm()
        if form.validate_on_submit():
            if not Employee.query.filter_by(Role="Admin").first():
                Admin_to_add=Employee( First_Name = form.First_Name.data,Last_Name = form.Last_Name.data,
                                   Email = form.Email.data,PhoneNumber = form.Phone_Number.data,
                                   DOB = form.DOB.data,Address = form.Address.data,
                                   password_hash = form.Password.data,Role="Admin" )
                db.session.add(Admin_to_add)
                db.session.commit()
                flash(f"Login to continue!!", category='success')
                return redirect(url_for('login'))
            else:
                flash(f'Sorry,Already Admin Exists. Please Login!', category='danger')
                return redirect(url_for('login'))
        if form.errors !={}:
            print(form.errors)
            for err_msg in form.errors.values():
                flash(f'there was a error in creating Admin :{err_msg}',category='danger')
        return render_template('register.html',form=form )
    else:
        return redirect('login')
@app.route('/get_token')
@login_required
def Get_token():
    return {'token': session.get('token')}
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():

        attempted_user = Employee.query.filter_by(Email=form.Email.data,Role=form.Role.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.Password.data
        ):
            login_user(attempted_user)
            auth = request.authorization
            token = jwt.encode({'Email': form.Email.data,'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)} ,app.config['SECRET_KEY'], 'HS256')
            session["token"]=token
            flash(f'Success! You are Logged as {attempted_user.Role} :{attempted_user.First_Name}', category='primary')
            return redirect('home')
        else:
            flash('Email and password are not matching! Please try again.',category='danger')
            return redirect('login')

    return render_template('login.html',form=form)





@app.route('/Employee_Master',methods=['GET','POST'])
@login_required
def Employee_Master():
    if admin_access():
        response={}
        employees=Employee.query.all()
        form=SearchForm()
        if form.validate_on_submit():
            if form.First_Name.data=='' and form.Address.data=='':
                response = requests.get("http://127.0.0.1:5000/search",headers={'x-access-token':session['token']})
                response = response.json()
                form.First_Name.data = ""
                form.Address.data = ""
                flash(f'Getting all The Employees', category='primary')
                print(response)
            elif form.First_Name.data!='' and form.Address.data!='':
                response = requests.get(f"http://127.0.0.1:5000/search/{form.First_Name.data}/{form.Address.data}",headers={'x-access-token':session['token']})
                response = response.json()
                flash(f'Getting The Selected Employees having {form.First_Name.data} and {form.Address.data} ', category='primary')
                form.First_Name.data=""
                form.Address.data=""
                print(response)

            else:
                form.First_Name.data = ""
                form.Address.data = ""
                flash(f'ERROR Accured!.So,Getting all The Employees', category='primary')
        flash("submit empty form to get all employees", category='primary')
        return render_template('Employee_Master.html', employees=employees, form=form, response=response)
    else:
        return redirect('Employee_details')

@app.route('/Employee_details')
@login_required
def Employee_details():
    return render_template('Employee_details.html')

@app.route('/Employee_registration',methods=['GET','POST'])
@login_required
def Employee_registration():
    if admin_access():
        form=RegistrationForm()
        if form.validate_on_submit():
            if Employee.query.filter_by(Email=form.Email.data).all():
                flash(f'SORRY! Email id already taken!!', category='danger')
                return redirect(url_for('Employee_registration'))
            else:
                Employee_to_add=Employee( First_Name = form.First_Name.data,Last_Name = form.Last_Name.data,
                                   Email = form.Email.data,PhoneNumber = form.Phone_Number.data,
                                   DOB = form.DOB.data,Address = form.Address.data,
                                   password_hash = form.Password.data ,Role="Employee")
                db.session.add(Employee_to_add)
                db.session.commit()
                flash(f'Successfully added employee', category='primary')
                return redirect(url_for('Employee_registration'))
        if form.errors !={}:
            print(form.errors)
            for err_msg in form.errors.values():
                flash(f'there was a error in creating Employee :{err_msg}',category='danger')

        return render_template('Employee_registration.html',form=form)
    else:
        return redirect('Employee_details')

def admin_access():
    if current_user.Role=="Employee":
        flash(f'Sorry, access denied!',category="danger")
        return False
    else:
        return True

def check_Admin_Available():
    if Employee.query.filter_by(Role="Admin").first():
        flash(f'Sorry,Already Admin Exists. Please Login!', category="danger")
        return False
    else:
        return True
@app.route('/clear_database')
@login_required
def clear_database():
    if admin_access():
        db.drop_all()
        db.create_all()
        flash("Successfully! Cleared Database.",category="success")
        return redirect('logout')
    return redirect('home')
@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('You have Successfully Logged out',category='info')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not Found",}
@app.errorhandler(500)
def handle_exception(err):
    return {'error':"Unknown Error"}
