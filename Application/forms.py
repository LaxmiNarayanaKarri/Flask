from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField,DateField,IntegerField,EmailField,SelectField
from wtforms.validators import Length,EqualTo,DataRequired,Email,ValidationError

class RegistrationForm(FlaskForm):
    def validate_Phone_Number(self,number):
        s=str(number.data)
        if len(s)!=10:
            raise ValidationError(f"Length of Phone Number should be 10.{s}")
    First_Name = StringField(validators=[DataRequired(),Length(min=2,max=15)])
    Last_Name = StringField(validators=[DataRequired(),Length(min=2,max=15)])
    Email = EmailField(validators=[DataRequired(),Email()])
    Phone_Number = IntegerField(validators=[DataRequired()])
    DOB = DateField(validators=[DataRequired()])
    Address = StringField(validators=[DataRequired(),Length(min=10,max=40)])
    Password = PasswordField(validators=[DataRequired(),Length(max=30)])
    Password2 = PasswordField(validators=[DataRequired(),EqualTo('Password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    Email = EmailField(validators=[DataRequired(), Email()])
    Role = SelectField(u'Role',choices=[('Admin','Admin'),('Employee','Employee')])
    Password = PasswordField(validators=[DataRequired(), Length(max=30)])

    submit = SubmitField()

class SearchForm(FlaskForm):
    First_Name = StringField()
    Address = StringField()
    submit = SubmitField()
