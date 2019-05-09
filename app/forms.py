from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, DateField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    email = StringField('Email address',
                        validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'),
                                    Length(max=50)])
    password = PasswordField('Password',
                             validators=[InputRequired("Please insert a valid password."), Length(min=3, max=80)])
    remember = BooleanField('remember me')


class Search(FlaskForm):
    page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    search_name = StringField(label='Book Name: ', validators=[Optional()])
    search_author = StringField(label='Author Name: ', validators=[Optional()])
    search_type = StringField(label='Type: ', validators=[Optional()])
    search_substring = BooleanField('Search sub-string')
    exclude_wishlist = BooleanField('Exclude wishlist')
    exclude_current_book = BooleanField('Exclude not returned book')
    only_available = BooleanField('Only available')
    def validate(self):
        if not super(Search, self).validate():
            return False
        if not self.search_name.data and not self.search_author.data and not self.search_type.data:
            msg = 'At least one of fields can not be empty!'
            self.search_name.errors.append(msg)
            return False
        return True


class Wishlist_form(FlaskForm):
    days_number = DecimalField(label="Number of days: ",
                               validators=[InputRequired("Must be a positive number"), NumberRange(min=1)])
    book_id = DecimalField(validators=[InputRequired("Missing book id")])
    rank = DecimalField(label="Rank", validators=[InputRequired("Rank out of range"), NumberRange(min=1)])


class Reserved_book_date(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',validators=[InputRequired("Date required!")])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[InputRequired("Date required!")])
    book_id_reserved = DecimalField(validators=[InputRequired("Missing book id"), NumberRange(min=1)])

    def validate(self):
        if not super(Reserved_book_date, self).validate():
            return False
        if self.startdate.data > self.enddate.data:
            msg = 'Start date can not be bigger than end date!'
            self.startdate.errors.append(msg)
            return False
        return True
