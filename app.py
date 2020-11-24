import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from passlib.hash import pbkdf2_sha256
import uuid
from flask_pymongo import PyMongo
from functools import wraps
from datetime import date
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


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    if request.method == "GET":
        return render_template("edit_profile.html")
    else:
        return User().edit_profile(username)


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
    tickets = Ticket().get_tickets()
    return render_template("dashboard.html", tickets=tickets)


@ app.route('/new_ticket', methods=['GET', 'POST'])
def new_ticket():
    if request.method == "GET":
        return render_template("new_ticket.html")
    else:
        return Ticket().new_ticket()


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
        if mongo.db.users.find_one({"username": user["username"]}):
            flash("Username address already in use")
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

    def edit_profile(self, username):

        if "profile_picture" in request.files:
            profile_picture = request.files["profile_picture"]
            mongo.save_file(profile_picture.filename, profile_picture)
        else:
            profile_picture.filename = ""

        user = {
            "username": username,
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


class Ticket:
    def new_ticket(self):
        date_created = date.today().strftime("%b %d, %Y")

        is_urgent = "on" if request.form.get("is_urgent") else "off"

        if mongo.db.tickets.count() == 0:
            ticket_number = 1
        else:
            ticket_number = mongo.db.tickets.count() + 1

        ticket = {
            "_id": uuid.uuid4().hex,
            "ticket_number": ticket_number,
            "title": request.form["title"],
            "status": "open",
            "date_created": date_created,
            "due_date": request.form["due_date"],
            "submited_by": session["user"]["username"],
            "is_urgent": is_urgent,
            "description": request.form["description"]
        }

        if mongo.db.tickets.insert_one(ticket):
            flash("Ticket created successfully.")
            return redirect("/dashboard")

        flash("Ticket creation failed.")

    def get_tickets(self):
        tickets = list(mongo.db.tickets.find())
        return tickets


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
