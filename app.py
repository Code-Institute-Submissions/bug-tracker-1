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


@app.route("/demo_login", methods=["GET", "POST"])
def demo_login():
    return User().demo_login()


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


@app.route('/delete/user/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    return User().delete_user(user_id=user_id)


@app.route('/file/<filename>')
@login_required
def file(filename):
    return mongo.send_file(filename)


@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    return render_template("profile.html")


@app.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket().get_tickets()
    return render_template("dashboard.html", tickets=tickets)


@app.route('/new_ticket', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == "GET":
        return render_template("new_ticket.html")
    else:
        return Ticket().new_ticket()


@app.route('/ticket/<ticket_id>', methods=['GET', 'POST'])
@login_required
def get_ticket_details(ticket_id):

    return Ticket().get_ticket_details(ticket_id=ticket_id)


@app.route('/ticket/update/<ticket_id>', methods=['GET', 'POST'])
@login_required
def update_ticket_status(ticket_id):
    return Ticket().update_ticket_status(ticket_id=ticket_id)


@app.route('/ticket/delete/<ticket_id>', methods=['GET', 'POST'])
@login_required
def delete_ticket(ticket_id):
    return Ticket().delete_ticket(ticket_id=ticket_id)


@app.route('/stats')
@login_required
def stats():
    return render_template("stats.html")


@app.route("/search_ticket", methods=["GET", "POST"])
def search_ticket():
    query = request.form.get("search-tab")
    tickets = list(mongo.db.tickets.find({"$text": {"$search": query}}))
    if len(tickets) == 0:
        flash("No tickets found.")
    return render_template("dashboard.html", tickets=tickets)


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

        flash("Wrong username or password.")
        return redirect(url_for("login"))

    def logout(self):
        session.clear()
        flash("You have been logged out")
        return redirect(url_for("login"))

    def edit_profile(self, username):

        currentUser = mongo.db.users.find_one({'username': username})
        newPassword = currentUser["password"]
        if pbkdf2_sha256.verify(request.form["password"], currentUser["password"]) == False:
            if request.form["password"] == "":
                newPassword = (currentUser["password"])
            else:
                newPassword = pbkdf2_sha256.hash(request.form["password"])

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
            "password": newPassword,
            "profile_picture_name": profile_picture.filename
        }

        dbResponse = mongo.db.users.update_one(
            {'username': username},
            {"$set": user})

        if dbResponse.modified_count == 1:
            flash("Profile updated successfully")
            User().start_session(user)

        return render_template("edit_profile.html")

    def delete_user(self, user_id):
        mongo.db.users.remove({"_id": user_id})
        flash("Account deleted successfully.")
        return redirect("/login")

    def demo_login(self):
        user = mongo.db.users.find_one({"username": "Demo"})
        return self.start_session(user)


class Ticket:
    def new_ticket(self):

        if "attachment" in request.files:
            attachment = request.files["attachment"]
            mongo.save_file(attachment.filename, attachment)

        date_created = date.today().strftime("%d/%m/%Y")

        is_urgent = "on" if request.form.get("is_urgent") else "off"

        if mongo.db.tickets.count() == 0:
            ticket_number = 1
        else:
            ticket_number = mongo.db.tickets.count() + 1

        ticket = {
            "_id": uuid.uuid4().hex,
            "ticket_number": ticket_number,
            "title": request.form["title"],
            "status": "Open",
            "date_created": date_created,
            "due_date": request.form["due_date"],
            "submited_by": session["user"]["username"],
            "is_urgent": is_urgent,
            "description": request.form["description"],
            "attachment_name": attachment.filename,
        }

        if mongo.db.tickets.insert_one(ticket):
            flash("Ticket created successfully.")
            return redirect("/dashboard")

        flash("Ticket creation failed.")

    def get_tickets(self):
        tickets = list(mongo.db.tickets.find())
        return tickets

    def get_ticket_details(self, ticket_id):
        ticket = mongo.db.tickets.find_one({"_id": ticket_id})
        return render_template('ticket.html', ticket=ticket)

    def update_ticket_status(self, ticket_id):
        dbResponse = mongo.db.tickets.update_one(
            {'_id': ticket_id},
            {"$set": {"status": request.form["ticket_status"]}})

        if dbResponse.modified_count == 1:
            flash(("Ticket Status Updated Successfully"))
            ticket = mongo.db.tickets.find_one({"_id": ticket_id})
            return render_template('ticket.html', ticket=ticket)

        flash(("Failed to update ticket."))
        return render_template('ticket.html', ticket=ticket)

    def delete_ticket(self, ticket_id):
        mongo.db.tickets.remove({"_id": ticket_id})
        flash("Ticket deleted successfully.")
        return redirect("/dashboard")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
