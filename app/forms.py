
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired("Please insert a valid password."), Length(min=3, max=80)])
    remember = BooleanField('remember me')

class SearchForm(FlaskForm):
    option = RadioField('Label', choices=[('1', 'Name'), ('2', 'Type'), ('3', 'Author')])
    autocomp = StringField('Search', id='name_autocomplete',validators=[InputRequired("Field can not be empty!"),Length(max=50)])

