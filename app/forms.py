from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, DateField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional
from app.models import BookTypes

class LoginForm(FlaskForm):
    email = StringField('Email address',
                        validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'),
                                    Length(max=50)])
    password = PasswordField('Password',
                             validators=[InputRequired("Please insert a valid password."), Length(min=3, max=80)])
    remember = BooleanField('remember me')


class Basic_search(FlaskForm):
    basic_page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    basic_search_name = StringField(label='Book Name: ', validators=[InputRequired("Book name is required!")])
    basic_search_substring = BooleanField('Search sub-string')


class Advanced_search(FlaskForm):
    page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    search_name = StringField(label='Book Name : ', validators=[Optional()])
    search_author_first_name = StringField(label='Author first name : ', validators=[Optional()])
    search_author_last_name = StringField(label='Author last name : ', validators=[Optional()])
    search_type = StringField(label='Type : ', validators=[Optional()])
    search_substring = BooleanField('Search sub-string')
    exclude_wishlist = BooleanField('Exclude wishlist')
    exclude_current_book = BooleanField('Exclude unreturned book')
    only_available = BooleanField('Only available')

    def validate(self):
        if not super(Advanced_search, self).validate():
            return False
        if not self.search_name.data and not self.search_author_first_name.data and not self.search_author_last_name.data and not self.search_type.data:
            msg = 'At least one of fields can not be empty!'
            self.search_name.errors.append(msg)
            return False
        return True


class Advanced_search_admnin(FlaskForm):
    page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    search_name = StringField(label='Book Name : ', validators=[Optional()])
    search_author_first_name = StringField(label='Author first name : ', validators=[Optional()])
    search_author_last_name = StringField(label='Author last name : ', validators=[Optional()])
    search_type = StringField(label='Type : ', validators=[Optional()])
    search_substring = BooleanField('Search sub-string')
    only_unreturned = BooleanField('Only unreturned book')
    only_available = BooleanField('Only available')

    def validate(self):
        if not super(Advanced_search_admnin, self).validate():
            return False
        if not self.search_name.data and not self.search_author_first_name.data and not self.search_author_last_name.data and not self.search_type.data:
            msg = 'At least one of fields can not be empty!'
            self.search_name.errors.append(msg)
            return False
        return True


class Wishlist_form(FlaskForm):
    days_number = DecimalField(label="Number of days : ",
                               validators=[InputRequired("Must be a positive number"), NumberRange(min=1)])
    book_id = DecimalField(validators=[InputRequired("Missing book id")])
    rank = DecimalField(label="Rank : ", validators=[InputRequired("Rank out of range"), NumberRange(min=1)])


class Reserved_book_date(FlaskForm):
    start_date = DateField('Start date : ', format='%Y-%m-%d', validators=[InputRequired("Date required!")])
    end_date = DateField('End date : ', format='%Y-%m-%d', validators=[InputRequired("Date required!")])
    book_id_reserved = DecimalField(validators=[InputRequired("Missing book id"), NumberRange(min=1)])

    def validate(self):
        if not super(Reserved_book_date, self).validate():
            return False
        if self.start_date.data >= self.end_date.data:
            msg = 'Invalid start date!'
            self.start_date.errors.append(msg)
            return False
        return True


class Wishlist_settings(FlaskForm):
    setting_option = RadioField('After failed to accept the given book : ',
                                choices=[('1', "Don`t change the wishlist state"), ('2', 'Remove the book'),
                                         ('3', 'Add it to the end of the wishlist')], validators=[InputRequired()])


class Change_password(FlaskForm):
    old_password = PasswordField('Old password: ',
                                 validators=[InputRequired("Field can not be empty !"), Length(min=3, max=80)])
    new_password = PasswordField('New password: ',
                                 validators=[InputRequired("Field can not be empty !"), Length(min=3, max=80)])
    retype_password = PasswordField('Retype password: ',
                                    validators=[InputRequired("Field can not be empty !"), Length(min=3, max=80)])

    def validate(self):
        if not super(Change_password, self).validate():
            return False
        if self.new_password.data != self.retype_password.data:
            msg = 'The password do not match!'
            self.new_password.errors.append(msg)
            self.retype_password.errors.append(msg)
            return False
        return True


class Profile(FlaskForm):
    first_name = StringField(label='First Name: ', validators=[InputRequired('Field can not be empty !')])
    last_name = StringField(label='First Name: ', validators=[InputRequired('Field can not be empty !')])
    email = StringField('Email address',validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'),
                                    Length(max=50)])
    library_card_id = StringField(label='Library Card Id : ', validators=[InputRequired('Field can not be empty !')])
    city = StringField(label='City: ', validators=[InputRequired('Field can not be empty !')])
    country = StringField(label='Country: ', validators=[InputRequired('Field can not be empty !')])
    zip_code = StringField(label='Postal Code: ', validators=[InputRequired('Field can not be empty !')])
    address = StringField(label='Address: ', validators=[InputRequired('Field can not be empty !')])

class Accept_next_book(FlaskForm):
    next_book_id = DecimalField(validators=[InputRequired("Missing book id"), NumberRange(min=1)])


class New_Book(FlaskForm):
    name = StringField(label='Book name: ', validators=[InputRequired('Field can not be empty !')])
    type_string_field = StringField(label='Book type: ',validators=[Optional()])
    type = SelectField(
        'Book type: ',
        choices=[(str(type.id), type.type_name) for type in BookTypes.query.order_by('type_name')],
        validators=[Optional()]
    )
    type_exists = RadioField(choices=[('1', "Type already exists"), ('2', 'New type')], validators=[InputRequired()])

    author_first_name = StringField(label='Author first name: ', validators=[InputRequired('Field can not be empty !')])
    author_last_name = StringField(label='Author last name: ', validators=[InputRequired('Field can not be empty !')])
    series = StringField(label='Book series: ', validators=[InputRequired('Field can not be empty !')])
    type_author = RadioField(choices=[('1', "New author"), ('2', 'Already exists')], validators=[InputRequired()])

    def validate(self):
        if not super(New_Book, self).validate():
            return False
        if not self.type_string_field.data and not self.type.data:

            msg = 'Field can not be empty !'
            self.type_string_field.errors.append(msg)
            self.type.errors.append(msg)
            print("msg"+msg)
            return False
        return True


class Choose_Author(FlaskForm):
    author_name = StringField(label='Author first name: ', validators=[InputRequired('Field can not be empty !')])
    page_nr = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    search_substring = BooleanField('Search sub-string')


class New_author(FlaskForm):
    new_author_first_name = StringField(label='First name: ', validators=[InputRequired('Field can not be empty !')])
    new_author_last_name = StringField(label='Last name: ', validators=[InputRequired('Field can not be empty !')])