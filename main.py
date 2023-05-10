from os import getenv
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

app.secret_key = getenv("APP_SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

app.permanent_session_lifetime = timedelta(minutes=5)


db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html", state="Testing")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True

        form_user = request.form["name"]

        found_user = Users.query.filter_by(name=form_user).first()
        if found_user:
            session["user"] = form_user
            session["email"] = found_user.email

        else:
            new_user = Users(form_user, "")
            db.session.add(new_user)
            db.session.commit()

            session["user"] = new_user.name
            session["email"] = ""

        flash("Login Successful!")

        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged In!")

            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods=["GET", "POST"])
def user():
    email = None
    logged_user = None

    if "user" in session:
        if request.method == "POST":
            email = request.form["email"]

            logged_user = session["user"]
            found_user = Users.query.filter_by(name=logged_user).first()
            found_user.email = email
            db.session.commit()

            session["email"] = email

            flash("Email was saved!")

        elif "email" in session:
            logged_user = session["user"]
            email = session["email"]

        return render_template("user.html", logged_user=logged_user, email=email)

    else:
        flash("You're not Logged In!")

        return redirect(url_for("login"))


@app.route("/users")
def users():
    return render_template("view.html", values=Users.query.all())


@app.route("/logout")
def logout():
    if "user" in session:
        logged_user = session["user"]

        flash(f"You have been logged out!, {logged_user}", "info")

    session.pop("user", None)
    session.pop("email", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
