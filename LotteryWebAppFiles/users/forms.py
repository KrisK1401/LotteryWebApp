from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, ValidationError, EqualTo
import re


# certain special charecters are not allowed in our requirements
def character_check(form, field):
    excluded_chars = "*?!'^+%&/()={[]}$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")



# Login in form that anonymous user fills with his information, if he already has an account
class LoginForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required()])
    submit = SubmitField()


# class for our ain registration fields, each having it own validators as given by the requirements
class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required()])
    lastname = StringField(validators=[Required()])
    phone = StringField(validators=[Required()])
    password = PasswordField(validators=[Required(), Length(min=6, max=12,
                                                            message='Password must be between 6 and 12 characters in length.')])
    confirm_password = PasswordField(
        validators=[Required(), EqualTo('password', message="Confirm password does not match the initial password")])
    pin_key = StringField(
        validators=[Required(), character_check, Length(max=32, min=32, message="Length of PIN key must be 32.")])
    submit = SubmitField()

    # validating the password, at least one digit, upper and lower case, and special characters for increased secuirity
    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*\W)')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 upper case, 1 lower case, and 1 special character.")


    # validating the phone number, checking if it's in XXXX - XXX - XXXX format
    def validate_phone(self, phone):
        p = re.compile(r'\d\d\d\d-\d\d\d-\d\d\d\d')
        if not p.match(self.phone.data):
            raise ValidationError("Phone number is not in the right format, xxxx-xxx-xxxx")
