from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.lift.models import Bench, Squat, Dead
from application.lift.forms import LiftForm


@app.route("/bench/", methods=["GET"])
@login_required(role="ANY")
def bench_index():

    return render_template("lift/list.html", benches=Bench.find_lifts(), squats=Squat.find_lifts(), deads=Dead.find_lifts())


@app.route("/bench/new/", methods=["GET"])
@login_required(role="ANY")
def bench_form():

    return render_template("lift/new.html", form=LiftForm())


@app.route("/bench/delete/<id>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_delete(id, lift_type):

    if lift_type == "bench":
        t = Bench.query.get(id)
    elif lift_type == "squat":
        t = Squat.query.get(id)
    else:
        t = Dead.query.get(id)
    if t.account_id != current_user.id:
        return login_manager.unauthorized()

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("bench_index"))


@app.route("/bench/change/<id>/<public>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_change(id, public,  lift_type):

    print("HGei")
    if lift_type == "bench":
        t = Bench.query.get(id)
    elif lift_type == "squat":
        t = Squat.query.get(id)
    else:
        t = Dead.query.get(id)
    if t.account_id != current_user.id:
        return login_manager.unauthorized()
    print("Hui")

    if public == "Yes":
        t.public = False
    else:
        t.public = True

    db.session().commit()
    print("Hai")

    return redirect(url_for("bench_index"))


@app.route("/bench/", methods=["POST"])
@login_required(role="ANY")
def bench_create():
    form = LiftForm(request.form)

    if not form.validate():
        return render_template("lift/new.html", form=form)

    print(form.lifts.data)
    if form.lifts.data == "bench":
        t = Bench(form.weight.data, form.date.data, form.public.data)
    elif form.lifts.data == "squat":
        t = Squat(form.weight.data, form.date.data, form.public.data)
    else:
        t = Dead(form.weight.data, form.date.data, form.public.data)

    t.account_id = current_user.id
    db.session().add(t)
    db.session().commit()

    return redirect(url_for("bench_index"))
