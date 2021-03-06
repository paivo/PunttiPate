from flask import render_template
from application import app
from application.lift.models import Bench, Squat, Dead
from application.gym.models import Gym


@app.route('/')
def index():
    return render_template("index.html", gyms=Gym.top(), benches=Bench.find_best(), squats=Squat.find_best(), deads=Dead.find_best())
