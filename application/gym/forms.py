from flask_wtf import FlaskForm
from wtforms import StringField, validators


class GymForm(FlaskForm):
    name = StringField("Other:", [validators.Length(min=3, max=50, message="Name must be between 3 to 50 characters.")])

    class Meta:
        csrf = False


class GymNameForm(FlaskForm):
    name = StringField("New name:", [validators.Length(min=3, max=50, message="Name must be between 3 to 50 characters.")])

    class Meta:
        csrf = False
