from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, RadioField, BooleanField, validators


class LiftForm(FlaskForm):
    lifts = RadioField(choices=[('bench', 'Benchpress'), ('squat', 'Squat'), ('dead', 'Deadlift')])
    weight = IntegerField("Weight", [validators.NumberRange(min=1, max=1000)])
    date = DateField("Date", format='%d.%m.%Y')
    public = BooleanField('Public')

    class Meta:
        csrf = False


class GymForm(FlaskForm):
    name = StringField("Other:", [validators.Length(min=3, max=50, message="Name must be between 3 to 50 characters.")])

    class Meta:
        csrf = False
