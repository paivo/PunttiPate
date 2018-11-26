from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_manager, login_required
from application.lift.models import Bench
from application.lift.forms import LiftForm


@app.route("/bench/", methods=["GET"])
@login_required(role="ANY")
def bench_index():
    return render_template("lift/list.html", benches=Bench.query.all())


@app.route("/bench/new/", methods=["GET"])
@login_required(role="ANY")
def bench_form():
    return render_template("bench/new.html", form=LiftForm())


@app.route("/bench/delete/<bench_id>/", methods=["POST"])
@login_required(role="ANY")
def bench_delete(bench_id):
    t = Bench.query.get(bench_id)
    if t.account_id != current_user.id:
        return login_manager.unauthorized()

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("bench_index"))


@app.route("/bench/", methods=["POST"])
@login_required(role="ANY")
def bench_create():
    form = LiftForm(request.form)

    if not form.validate():
        return render_template("bench/new.html", form=form)

    t = Bench(form.name.data)
    t.done = form.done.data
    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("bench_index"))
