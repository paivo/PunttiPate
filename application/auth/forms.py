from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


# Kirjautuminen
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


# Rekisteröityminen
class SignupForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=5, max=50, message="Name must be between 5 to 50 characters.")])
    username = StringField("Username", [validators.Length(min=3, max=10
                                        , message="Userame must be between 3 to 10 characters.")])
    password = PasswordField("Password", [validators.Length(min=5, max=50
                                        , message="Password must be between 5 to 50 characters.")])
    confirm = PasswordField("Repeat password")

    class Meta:
        csrf = False


# Salasanan vaihto
class PasswordForm(FlaskForm):
    old_password = PasswordField("Old password", [validators.Length(min=5, max=50)])
    new_password = PasswordField("New password", [validators.Length(min=5, max=50)])
    passwordConfirmation = PasswordField(
        "Repeat new password", [validators.Length(min=8, max=50), validators.EqualTo("new_password", message="Passwords do not match.")])
