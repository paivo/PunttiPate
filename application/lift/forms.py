from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, RadioField, BooleanField, validators
from wtforms.validators import DataRequired


class LiftForm(FlaskForm):
    lifts = RadioField(choices=[('bench', 'Benchpress'), ('squat', 'Squat'), ('dead', 'Deadlift')], validators=[DataRequired()])
    weight = IntegerField("Weight", [validators.NumberRange(min=1, max=1000)])
    date = DateField("Date", format='%d.%m.%Y', validators=[DataRequired()])
    public = BooleanField('Public')

    class Meta:
        csrf = False
