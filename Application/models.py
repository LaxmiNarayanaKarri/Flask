from Application import db,login_manager
from Application import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Employee(db.Model,UserMixin):
    id = db.Column( db.Integer(), primary_key=True)
    First_Name = db.Column(db.String(length=15))
    Last_Name = db.Column(db.String(length=15))
    Email = db.Column(db.String(length=30),unique=True)
    PhoneNumber = db.Column(db.Integer())
    DOB = db.Column(db.DateTime())
    Address = db.Column(db.String(length=40))
    password = db.Column(db.String(length=30))
    Role = db.Column(db.String(length=8))

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self,password_old):
        self.password = bcrypt.generate_password_hash(password_old).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


