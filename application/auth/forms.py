from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from wtforms.validators import InputRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password", [validators.Length(min=3)])

    class Meta:
        csrf = False


class SignupForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
    username = StringField("Username", [validators.Length(min=3)])
    password = PasswordField("Password", [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Repeat password")

    class Meta:
        csrf = False
