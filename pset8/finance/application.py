import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    uid = session["user_id"]

    rows = db.execute("SELECT symbol, \
                       SUM(case when tx_type = 0 THEN shares ELSE -1 * shares END) as num_shares, \
                       SUM(case when tx_type=0 THEN shares * price ELSE -1 * shares * price END) as net_cost \
                       FROM holdings \
                       WHERE user_id = :uid \
                       GROUP BY symbol \
                       HAVING num_shares > 0", uid=uid)
    user = db.execute("SELECT cash from users where id = :uid", uid=uid)
    cash = user[0]["cash"]
    return render_template("index.html", rows=rows, cash=cash, lookup=lookup)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # checking for blank fields
        if not request.form.get("symbol"):
            return apology("Symbol field cannot be blank")
        elif not request.form.get("shares"):
            return apology("Number of shares cannot be blank")

        else:
            symbol = request.form.get("symbol").upper()
            try:
                amount = int(request.form.get("shares"))
            except TypeError:
                return apology("PLease enter a positive integer")
            stock = lookup(symbol)
            query = db.execute("SELECT cash from users where id = :userid", userid=session["user_id"])
            balance = float(query[0]["cash"])

            # check whether they have enough to execute trade
            cost = stock["price"] * amount
            if balance < cost:
                return apology("you do not have enough funds to complete the purchase")
            else:
                # add transaction to holdings table
                db.execute("INSERT INTO holdings (user_id, tx_type, symbol, shares, price) VALUES(:userid, :tx_type, :symbol, :shares, :price)"
                            ,userid=session["user_id"], tx_type=0, symbol=symbol, shares=amount, price=stock["price"])

                # update cash balance in user table
                db.execute("UPDATE users SET cash = :value WHERE id = :userid", value=(balance - cost), userid=session["user_id"])

                # navigate to index page
                return render_template("index.html")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT timestamp, symbol, \
                        CASE WHEN tx_type = 0 THEN :buy else :sell END as trade, \
                        shares, price \
                        FROM holdings where user_id = :uid \
                        ORDER BY timestamp", uid=session['user_id'], buy="bought", sell="sold")

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # check whether they've entered a symbol
        if not symbol:
            return apology("must enter a symbol")

        else:
            symbol = symbol.upper()
            stock_data = lookup(symbol)

            return render_template("quoted.html", name=stock_data['name'], symbol=stock_data["symbol"], price=stock_data["price"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        import re

        uname = request.form.get("username")
        pw = request.form.get("password")

        # check whether username is blank
        if not uname:
            return apology("must specify a username", 403)

        # check whether password is blank
        elif not pw:
            return apology("password cannot be blank", 403)

        # check whether passwords are strong
        elif (len(pw) < 8) or (re.search(r"\d", pw) is None) or (re.search(r"[A-Z]", pw) is None) or (re.search(r"\W", pw) is None) or (re.search(r"[a-z]", pw) is None):
            return apology("Passwords must be at least 8 characters long, contain at least one uppercase and one \
            lower case letter and at least one special character.")


        # check whether passwords match
        elif pw != request.form.get("confirmation"):
            return apology("passwords do not match", 403)


        # check whether username already exists
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

            # if not then add to database
            if len(rows) == 0:
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashval)", username=request.form.get("username"), hashval=generate_password_hash(request.form.get("password")))
                return redirect("/")
            else:
                return apology("username already exists, please select another")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    uid = session["user_id"]

    if request.method == "POST":

        # check that option has been selected
        if request.form.get("symbol") == "Please Select:":
            return apology("please select a stock to sell")

        # check that number of shares has been selected
        elif not request.form.get("shares"):
            return apology("please enter the number of shares to sell")
        else:
            symbol = request.form.get("symbol").upper()
            try:
                shares = int(request.form.get("shares"))
            except TypeError:
                return apology("please enter an integer")

            holdings = db.execute("SELECT SUM(case when tx_type = 0 then shares else -1 * shares END) as num_shares \
                                    FROM holdings \
                                    WHERE symbol = :symbol and user_id = :uid", symbol=symbol, uid=uid)

            num_shares = holdings[0]['num_shares']
            if num_shares < shares:
                return apology("You only have {} shares of {}, please choose an amount less than or equal to that to sell".format(num_shares, symbol))
            else:
                stock = lookup(symbol)
                query = db.execute("SELECT cash from users where id = :userid", userid=uid)
                balance = float(query[0]["cash"])

                # add transaction to holdings table
                db.execute("INSERT INTO holdings (user_id, tx_type, symbol, shares, price) VALUES(:userid, :tx_type, :symbol, :shares, :price)"
                            ,userid=uid, tx_type=1, symbol=symbol, shares=shares, price=stock["price"])

                # update cash balance in user table
                rev = stock["price"] * shares
                db.execute("UPDATE users SET cash = :value WHERE id = :userid", value=(balance + rev), userid=session["user_id"])

                # navigate to index page
                return redirect("/")


    else:
        stocks = db.execute("SELECT DISTINCT symbol from holdings WHERE user_id = :uid ORDER BY symbol", uid=uid)
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
