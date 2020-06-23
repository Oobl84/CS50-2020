import os

from sqlalchemy import create_engine
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQL_alchemy to use SQLite database
engine = create_engine('sqlite:///habits.db')
conn = engine.connect()

# configure index functionality
@app.route("/")
@login_required
def index():

    return apology("this page not yet built")


# configure habits page
@app.route("/habits", methods=['GET', 'POST'])
@login_required
def habits():
    return apology("this page not yet built")

           # add habit

           # remove habit
# configure lifecal page
@app.route("/lifecal")
@login_required
def lifecal():
    return apology("this page not yet built")
    # render life calendar blocks

# configure login
@app.route("/login", methods=['GET','POST'])
def login():

    # forget any user data
    session.clear()

    if request.method == "POST":

        # check username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        # check password has been submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # check username and password
        # Query database for username
        rows = conn.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


# configure logout
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect usert to login form
    return redirect("/")

# configure register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        return apology("this page not yet built")

        # get user details
    else:
        return render_template("register.html")

def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
