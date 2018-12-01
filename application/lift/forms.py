from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, RadioField, validators


class LiftForm(FlaskForm):
    lifts = RadioField(choices=[('bench', 'Benchpress'), ('squat', 'Squat'), ('dead', 'Deadlift')])
    weight = IntegerField("Weight", [validators.NumberRange(min=1, max=1000)])
    date = DateField("Date", format='%d.%m.%Y')

    class Meta:
        csrf = False
