
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired("Please insert a valid password."), Length(min=3, max=80)])
    remember = BooleanField('remember me')