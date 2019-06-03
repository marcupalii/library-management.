from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DecimalField, DateField, RadioField, SelectField, FileField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional
from app.models import BookTypes
from flask_wtf.file import FileAllowed

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

class Update_book(FlaskForm):
    update_book_name = StringField(label='Book name : ', validators=[InputRequired()])
    update_book_type = StringField(label='Book type : ', validators=[InputRequired()])
    update_book_series = StringField(label='Book series : ', validators=[InputRequired()])
    update_author_first_name = StringField(label='Author first name : ', validators=[InputRequired()])
    update_author_last_name = StringField(label='Author last name : ', validators=[InputRequired()])
    update_book_series_id = DecimalField(validators=[InputRequired(), NumberRange(min=1)])

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
        if (not self.type_string_field.data and self.type_exists.data == '2')\
            or (not self.type.data and self.type_exists.data == '1'):

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




class Add_user(FlaskForm):
    file = FileField(label="Choose file...", validators=[InputRequired()])
    first_name = StringField(label='First Name: ', validators=[InputRequired('Field can not be empty !')])
    last_name = StringField(label='Last Name: ', validators=[InputRequired('Field can not be empty !')])
    email = StringField('Email address',validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'),
                                    Length(max=50)])
    library_card_id = StringField(label='Library Card Id : ', validators=[InputRequired('Field can not be empty !')])
    city = StringField(label='City: ', validators=[InputRequired('Field can not be empty !')])
    country = StringField(label='Country: ', validators=[InputRequired('Field can not be empty !')])
    zip_code = StringField(label='Postal Code: ', validators=[InputRequired('Field can not be empty !')])
    address = StringField(label='Address: ', validators=[InputRequired('Field can not be empty !')])


class Basic_search_users(FlaskForm):
    basic_page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    basic_search_name = StringField(label='Firs name or last name: ', validators=[InputRequired("Book name is required!")])
    basic_search_substring = BooleanField('Search sub-string')


class Advanced_search_users(FlaskForm):
    advanced_page_number = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    advanced_user_first_name = StringField(label='User first name : ', validators=[Optional()])
    advanced_user_last_name = StringField(label='User last name : ', validators=[Optional()])
    advanced_user_library_card_id = StringField(label='User library card id: ',validators=[Optional()])
    advanced_user_email = StringField('Email address : ',validators=[Optional()])

    search_substring = BooleanField('Search sub-string')

    def validate(self):
        if not super(Advanced_search_users, self).validate():
            return False
        if not self.advanced_user_first_name.data and not self.advanced_user_last_name.data and not self.advanced_user_library_card_id.data and not self.advanced_user_email.data:
            msg = 'At least one of fields can not be empty!'
            self.advanced_user_first_name.errors.append(msg)
            return False
        return True


class Update_user(FlaskForm):
    update_user_id = DecimalField(validators=[InputRequired(), NumberRange(min=1)])
    update_user_book_return_coeff = StringField(label='Book`s return coefficient: ', validators=[InputRequired('Field can not be empty !')])
    update_user_file = FileField(label="Choose file...", validators=[InputRequired()])
    update_user_first_name = StringField(label='First Name: ', validators=[InputRequired('Field can not be empty !')])
    update_user_last_name = StringField(label='Last Name: ', validators=[InputRequired('Field can not be empty !')])
    update_user_email = StringField('Email address',validators=[InputRequired("Please insert a valid email."), Email(message='Invalid email'),
                                    Length(max=50)])
    update_user_library_card_id = StringField(label='Library Card Id : ', validators=[InputRequired('Field can not be empty !')])
    update_user_city = StringField(label='City: ', validators=[InputRequired('Field can not be empty !')])
    update_user_country = StringField(label='Country: ', validators=[InputRequired('Field can not be empty !')])
    update_user_zip_code = StringField(label='Postal Code: ', validators=[InputRequired('Field can not be empty !')])
    update_user_address = StringField(label='Address: ', validators=[InputRequired('Field can not be empty !')])
    update_user_type = StringField(label='User type: ', validators=[InputRequired('Field can not be empty !')])

