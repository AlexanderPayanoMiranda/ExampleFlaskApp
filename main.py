from os import getenv
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("APP_SECRET")
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
    return render_template("index.html", state="Testing")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        form_user = request.form["name"]
        session["user"] = form_user
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        logged_user = session["user"]
        return render_template("user.html", user=logged_user)
    else:
        flash("You're not Logged In!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        logged_user = session["user"]
        flash(f"You have been logged out!, {logged_user}", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
