from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, db, login_manager, login_required
from application.lift.models import Bench, Squat, Dead, Gym, GymUser
from application.lift.forms import LiftForm, GymForm


## Luodaan gym tietokohde jos saman nimistä ei jo ole. Liitetään molemmissa tapauksissa kyseinen gym käyttäjään.
@app.route("/gym/create/", methods=["POST"])
@login_required(role="ANY")
def gym_create():
    form2 = GymForm(request.form)
    gym_name = form2.name.data

    if not form2.validate():
        return render_template("lift/new.html", form=LiftForm(), form2=form2, gyms=Gym.find_all())

    if gym_name not in Gym.find_all_names():
        gym = Gym(form2.name.data)
        db.session().add(gym)
        db.session().commit()

    return gym_add(Gym.find_one(gym_name)[0])


## Liitetään kyseinen gym käyttäjään.
@app.route("/gym/add/<id>/", methods=["POST"])
@login_required(role="ANY")
def gym_add(id):

    for user in GymUser.find_all():

        if int(user["gym_id"]) == int(id) and int(user["account_id"]) == int(current_user.id):
            return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all(),
                                    errormessage="You have already added this one.")

    gym_user = GymUser(id, current_user.id)
    db.session().add(gym_user)
    db.session().commit()
    return redirect(url_for("bench_index"))


## Haetaan kaikki kyseisen käyttäjän punttitulokset listattavaksi.
@app.route("/bench/", methods=["GET"])
@login_required(role="ANY")
def bench_index():

    return render_template("lift/list.html", benches=Bench.find_lifts(), squats=Squat.find_lifts(), deads=Dead.find_lifts())


## Haetaan punttikaavake, salikaavake ja kaikki jo luodut salit.
@app.route("/bench/new/", methods=["GET"])
@login_required(role="ANY")
def bench_form():

    return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all())


##Poista penkki, kyykky tai maastaveto tulos
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


## Vaihda punttitulos julkiseksi tai päinvastoin.
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


##Luo penkki, kyykky tai mave tulos.
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
