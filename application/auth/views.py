from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
  
from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, SignupForm


## Kirjautuminen
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                                error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))   


## Uloskirjautuminen
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))     


## Rekisteröityminen
@app.route("/auth/signup", methods = ["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signupform.html", form=SignupForm())

    form = SignupForm(request.form)

    if not form.validate():
        return render_template("auth/signupform.html", form=form)

    possible_username = User.query.filter_by(username=form.username.data).first()
    if possible_username:
        return render_template("auth/signupform.html", form=form, error="Username is already taken.")

    if form.password.data != form.confirm.data:
        return render_template("auth/signupform.html", form=form, error="Passwords do not match.")

    user = User(form.name.data)
    user.username = form.username.data
    user.password = form.password.data

    db.session().add(user)
    db.session().commit()
    login_user(user)

    return redirect(url_for("index"))   
