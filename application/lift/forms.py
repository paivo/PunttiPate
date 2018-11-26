from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, validators


class LiftForm(FlaskForm):
    weight = IntegerField("Weight", [validators.Length(min=1)])
    date = DateField("Date")

    class Meta:
        csrf = False
