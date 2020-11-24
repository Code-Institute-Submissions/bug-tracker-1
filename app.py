import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from passlib.hash import pbkdf2_sha256
import uuid
from flask_pymongo import PyMongo
from functools import wraps
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrapper


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    return User().login()


@app.route("/logout")
def logout():
    return User().logout()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        return User().signup()


@app.route('/forgot_password')
def forgot_password():
    return render_template("forgot_password.html")


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):

    if request.method == 'GET':
        return render_template("edit_profile.html")

    if "profile_picture" in request.files:
        profile_picture = request.files["profile_picture"]
        mongo.save_file(profile_picture.filename, profile_picture)
    else:
        profile_picture.filename = ""

    user = {
        "username": request.form["username"],
        "name": request.form["name"],
        "email": request.form["email"],
        "dob": request.form["dob"],
        "password": request.form["password"],
        "profile_picture_name": profile_picture.filename
    }

    dbResponse = mongo.db.users.update_one(
        {'username': username},
        {"$set": user})

    if dbResponse.modified_count == 1:
        flash("Profile updated successfully")
        User().start_session(user)

    return render_template("edit_profile.html")


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    return render_template("profile.html")


@ app.route('/dashboard')
@ login_required
def dashboard():
    return render_template("dashboard.html")


@ app.route('/new_ticket')
def new_ticket():
    return render_template("new_ticket.html")


@ app.route('/ticket')
def get_ticket():
    return render_template("ticket.html")


@ app.route('/stats')
def stats():
    return render_template("stats.html")


class User:

    def start_session(self, user):
        session["logged_in"] = True
        session["user"] = user
        return redirect("/dashboard")

    def signup(self):

        if "profile_picture" in request.files:
            profile_picture = request.files["profile_picture"]
            mongo.save_file(profile_picture.filename, profile_picture)
        else:
            profile_picture.filename = ""

        # Create User object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get("username"),
            "name": request.form.get("name"),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "profile_picture_name": profile_picture.filename
        }

        # Password Encryption.
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        # Check for duplicates.
        if mongo.db.users.find_one({"email": user["email"]}):
            flash("Email address already in use")
            return redirect(url_for("signup"))

        # Insert User in the Database
        if mongo.db.users.insert_one(user):
            return self.start_session(user)

        flash("Signup Failed")
        return redirect(url_for("signup"))

    def login(self):

        user = mongo.db.users.find_one({
            "username": request.form.get("username")
        })

        if user and pbkdf2_sha256.verify(request.form.get("password"), user["password"]):
            return self.start_session(user)

        flash("Signup Failed")
        return redirect(url_for("login"))

    def logout(self):
        session.clear()
        flash("You have been logged out")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
