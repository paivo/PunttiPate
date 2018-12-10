from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, db, login_manager, login_required
from application.lift.models import Bench, Squat, Dead, Gym, GymUser
from application.lift.forms import LiftForm, GymForm


@app.route("/gym/create/", methods=["POST"])
@login_required(role="ANY")
def gym_create():
    form2 = GymForm(request.form)
    gym_name = form2.name.data

    if not form2.validate():
        return render_template("lift/new.html", form=LiftForm(), form2=form2, gyms=Gym.find_all())

    if gym_name not in Gym.find_all():
        gym = Gym(form2.name.data)
        db.session().add(gym)
        db.session().commit()
    else:
        gym = Gym.find_one(gym_name)

    gym_user = GymUser(gym.id, current_user.id)
    db.session().add(gym_user)
    db.session().commit()

    return redirect(url_for("bench_index"))


@app.route("/gym/add/<id>/", methods=["POST"])
@login_required(role="ANY")
def gym_add(id):

    for user in GymUser.find_all():
        print(id, current_user.id)
        print(user["gym_id"], user["account_id"])
        if user["gym_id"] == id and user["account_id"] == current_user.id:
            return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all(),
                              error="You have already added this one.")

    gym_user = GymUser(id, current_user.id)
    db.session().add(gym_user)
    db.session().commit()
    return redirect(url_for("bench_index"))


@app.route("/bench/", methods=["GET"])
@login_required(role="ANY")
def bench_index():

    return render_template("lift/list.html", benches=Bench.find_lifts(), squats=Squat.find_lifts(), deads=Dead.find_lifts())


@app.route("/bench/new/", methods=["GET"])
@login_required(role="ANY")
def bench_form():

    return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all())


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

    if lift_type == "bench":
        t = Bench.query.get(id)
    elif lift_type == "squat":
        t = Squat.query.get(id)
    else:
        t = Dead.query.get(id)
    if t.account_id != current_user.id:
        return login_manager.unauthorized()

    if public == "Yes":
        t.public = False
    else:
        t.public = True

    db.session().commit()

    return redirect(url_for("bench_index"))


@app.route("/bench/", methods=["POST"])
@login_required(role="ANY")
def bench_create():
    form = LiftForm(request.form)

    if not form.validate():
        return render_template("lift/new.html", form=form, form2=GymForm(), gyms=Gym.find_all())

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
