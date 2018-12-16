from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, db, login_manager, login_required
from application.lift.models import Bench, Squat, Dead, Gym, GymUser
from application.lift.forms import LiftForm, GymForm, GymNameForm


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
@app.route("/gym/add/<gym_id>/", methods=["POST"])
@login_required(role="ANY")
def gym_add(gym_id):

    for user in GymUser.find_all():
        if int(user["gym_id"]) == int(gym_id) and int(user["account_id"]) == int(current_user.id):
            return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all(),
                                    errormessage="You have already joined this one.")

    gym_user = GymUser(gym_id, current_user.id)
    db.session().add(gym_user)
    db.session().commit()
    return redirect(url_for("gym_index"))


## Poistetaan kyseinen GymUser rivi.
@app.route("/gym/remove/<gym_id>", methods=["POST"])
@login_required(role="ANY")
def gym_remove(gym_id):
    GymUser.delete(gym_id)
    return redirect(url_for("gym_index"))


# Vaihda salin nimi.
@app.route("/gym/<gym_id>/", methods = ["GET", "POST"])
@login_required(role="ANY")
def gym_edit(gym_id):
    gym = Gym.query.get(gym_id)
    if request.method == "GET":
        return render_template("gym/edit.html", form=GymNameForm(), gym=gym)

    form = GymNameForm(request.form)
    if not form.validate():
        return render_template("gym/edit.html", form=form, gym=gym)
    gym.name = form.name.data
    db.session().commit()

    return redirect(url_for("gym_index"))


## Haetaan kaikki kyseisen käyttäjän salit listattavaksi.
@app.route("/gym/", methods=["GET"])
@login_required(role="ANY")
def gym_index():

    return render_template("gym/list.html", gyms=Gym.find_gyms_joined())



## Haetaan kaikki kyseisen käyttäjän punttitulokset listattavaksi.
@app.route("/bench/", methods=["GET"])
@login_required(role="ANY")
def bench_index():

    return render_template("lift/list.html", benches=Bench.find_lifts(), squats=Squat.find_lifts(), deads=Dead.find_lifts())


# Haetaan kyseinen punttitulos listattavaksi.
@app.route("/bench/view/<lift_id>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_view(lift_id, lift_type):
    if lift_type == "bench":
        lift = Bench.query.get(lift_id)
    elif lift_type == "squat":
        lift = Squat.query.get(lift_id)
    else:
        lift = Dead.query.get(lift_id)
    if lift.account_id != current_user.id:
        return login_manager.unauthorized()
    if lift.public:
        lift.public = "Yes"
    else:
        lift.public = "No"
    return render_template("lift/view.html", lift=lift, lift_type=lift_type)


# Haetaan punttikaavake, salikaavake ja kaikki jo luodut salit.
@app.route("/bench/new/", methods=["GET"])
@login_required(role="ANY")
def bench_form():

    return render_template("lift/new.html", form=LiftForm(), form2=GymForm(), gyms=Gym.find_all())


# Poista penkki, kyykky tai maastaveto tulos
@app.route("/bench/delete/<lift_id>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_delete(lift_id, lift_type):

    if lift_type == "bench":
        lift = Bench.query.get(lift_id)
    elif lift_type == "squat":
        lift = Squat.query.get(lift_id)
    else:
        lift = Dead.query.get(lift_id)
    if lift.account_id != current_user.id:
        return login_manager.unauthorized()

    db.session().delete(lift)
    db.session().commit()

    return redirect(url_for("bench_index"))


# Vaihda punttitulos julkiseksi tai päinvastoin listaus sivulla.
@app.route("/bench/change/<lift_id>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_change(lift_id,  lift_type):

    if lift_type == "bench":
        lift = Bench.query.get(lift_id)
    elif lift_type == "squat":
        lift = Squat.query.get(lift_id)
    else:
        lift = Dead.query.get(lift_id)
    if lift.account_id != current_user.id:
        return login_manager.unauthorized()

    if lift.public:
        lift.public = False
    else:
        lift.public = True

    db.session().commit()

    return redirect(url_for("bench_index"))


# Vaihda punttitulos julkiseksi tai päinvastoin yksittäisen tuloksen sivulla.
@app.route("/bench/change/single/<lift_id>/<lift_type>/", methods=["POST"])
@login_required(role="ANY")
def bench_change_single(lift_id, lift_type):
    if lift_type == "bench":
        lift = Bench.query.get(lift_id)
    elif lift_type == "squat":
        lift = Squat.query.get(lift_id)
    else:
        lift = Dead.query.get(lift_id)
    if lift.account_id != current_user.id:
        return login_manager.unauthorized()

    if lift.public:
        lift.public = False
    else:
        lift.public = True
    db.session().commit()
    if lift.public:
        lift.public = "Yes"
    else:
        lift.public = "No"

    return render_template("lift/view.html", lift=lift, lift_type=lift_type)


# Luo penkki, kyykky tai mave tulos.
@app.route("/bench/", methods=["POST"])
@login_required(role="ANY")
def bench_create():
    form = LiftForm(request.form)

    if not form.validate():
        return render_template("lift/new.html", form=form, form2=GymForm(), gyms=Gym.find_all())

    if form.lifts.data == "bench":
        lift = Bench(form.weight.data, form.date.data, form.public.data)
    elif form.lifts.data == "squat":
        lift = Squat(form.weight.data, form.date.data, form.public.data)
    else:
        lift = Dead(form.weight.data, form.date.data, form.public.data)

    lift.account_id = current_user.id
    db.session().add(lift)
    db.session().commit()

    return redirect(url_for("bench_index"))
