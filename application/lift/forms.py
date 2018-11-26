from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, validators


class LiftForm(FlaskForm):
    weight = IntegerField("Weight", [validators.NumberRange(min=1, max=1000)])
    date = DateField("Date", [validators.Required()], format='%d.%m.%Y')

    class Meta:
        csrf = False
