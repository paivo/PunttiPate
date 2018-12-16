from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, RadioField, BooleanField, validators


class LiftForm(FlaskForm):
    lifts = RadioField(choices=[('bench', 'Benchpress'), ('squat', 'Squat'), ('dead', 'Deadlift')])
    weight = IntegerField("Weight", [validators.NumberRange(min=1, max=1000)])
    date = DateField("Date", format='%Y-%m-%d')
    public = BooleanField('Public')

    class Meta:
        csrf = False

