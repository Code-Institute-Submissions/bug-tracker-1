import os
from flask import (
    Flask, flash, render_template, jsonify,
    redirect, request, session, url_for)
from passlib.hash import pbkdf2_sha256
import uuid
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


@app.route('/chart')
@login_required
def chart():
    tickets = Ticket().get_tickets()
    filtered = []
    for x in tickets:
        if x["submited_by"] == session["user"]["username"]:
            filtered.append(x)
    return jsonify(tickets, filtered)


@app.route('/stats')
@login_required
def stats():
    return render_template('stats.html')


@app.route("/search_ticket", methods=["GET", "POST"])
def search_ticket():
    query = request.form.get("search_tab")
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

        if ("profile_picture" in request.files):
            profile_picture = request.files["profile_picture"]
            if (profile_picture.filename != ""):
                profile_picture.filename = uuid.uuid4().hex
            else:
                profile_picture.filename = ""
            mongo.save_file(profile_picture.filename, profile_picture)

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

        elif mongo.db.users.find_one({"email": user["email"]}):
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

        flash("Wrong username or password.")
        return redirect(url_for("login"))

    def logout(self):
        session.clear()
        flash("You have been logged out")
        return redirect(url_for("login"))

    def edit_profile(self, username):
        currentUser = mongo.db.users.find_one({'username': username})
        new_email = currentUser["email"]
        new_password = currentUser["password"]

        if pbkdf2_sha256.verify(request.form["password"], currentUser["password"]) == False:
            if request.form["password"] == "":
                new_password = (currentUser["password"])
            else:
                new_password = pbkdf2_sha256.hash(request.form["password"])

        if ("profile_picture" in request.files) and (request.files["profile_picture"].filename != ""):
            profile_picture = request.files["profile_picture"]
            profile_picture.filename = uuid.uuid4().hex

            self.delete_files()
            mongo.save_file(profile_picture.filename, profile_picture)
            updated_picture = profile_picture.filename

        else:
            updated_picture = currentUser["profile_picture_name"]

        if (new_email != request.form["email"]) and (not mongo.db.users.find_one({"email": request.form["email"]})):
            new_email = request.form["email"]

        elif (new_email == request.form["email"]):
            new_email = request.form["email"]

        else:
            flash("Email address already in use")
            return render_template("edit_profile.html")

        user = {
            "username": username,
            "name": request.form["name"],
            "email": new_email,
            "dob": request.form["dob"],
            "password": new_password,
            "profile_picture_name": updated_picture
        }

        dbResponse = mongo.db.users.update_one(
            {'username': username},
            {"$set": user})

        if dbResponse.modified_count == 1:
            flash("Profile updated successfully")
            User().start_session(user)

        return render_template("edit_profile.html")

    def delete_user(self, user_id):

        self.delete_files()
        mongo.db.users.remove({"_id": user_id})

        flash("Account deleted successfully.")
        return redirect("/login")

    def demo_login(self):
        '''Log in as a demo user. This is for demonstration purposes only.'''

        user = mongo.db.users.find_one({"username": "Demo"})
        return self.start_session(user)

    def delete_files(self):
        '''This deletes all the chunks and files created 
        when a profile picture is inserted in the database'''

        if (mongo.db.fs.files.find_one({"filename": session["user"]["profile_picture_name"]})):
            old_file = mongo.db.fs.files.find_one(
                {"filename": session["user"]["profile_picture_name"]})
            mongo.db.fs.chunks.remove(
                {"files_id": ObjectId(old_file["_id"])})
            mongo.db.fs.files.remove(
                {"filename": session["user"]["profile_picture_name"]})


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
        if (len(request.form) <= 1):
            ticket = mongo.db.tickets.find_one({"_id": ticket_id})
            status = ticket["status"]
        else:
            status = request.form["ticket_status"]
        dbResponse = mongo.db.tickets.update_one(
            {'_id': ticket_id},
            {"$set": {"status": status,
                      "assigned_to": session["user"]["username"]
                      }
             })

        if dbResponse.modified_count == 1:
            flash(("Ticket Status Updated Successfully"))
            ticket = mongo.db.tickets.find_one({"_id": ticket_id})
            return render_template('ticket.html', ticket=ticket)
        else:
            flash(("Failed to update ticket."))
            ticket = mongo.db.tickets.find_one({"_id": ticket_id})

        return render_template('ticket.html', ticket=ticket)

    def delete_ticket(self, ticket_id):
        self.delete_attachment_files(ticket_id)
        mongo.db.tickets.remove({"_id": ticket_id})
        flash("Ticket deleted successfully.")
        return redirect("/dashboard")

    def delete_attachment_files(self, ticket_id):
        '''This deletes all the chunks and files created 
        when a attachment is inserted in the database'''

        ticket = mongo.db.tickets.find_one({"_id": ticket_id})

        if (mongo.db.fs.files.find_one({"filename": ticket["attachment_name"]})):
            old_file = mongo.db.fs.files.find_one(
                {"filename": ticket["attachment_name"]})
            mongo.db.fs.chunks.remove(
                {"files_id": ObjectId(old_file["_id"])})
            mongo.db.fs.files.remove(
                {"filename": ticket["attachment_name"]})


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
