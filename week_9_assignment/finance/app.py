import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
# Search history
history_search = []


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    symbols = db.execute("SELECT Symbol FROM {}".format(name[0]['username']))

    for symbol_data in symbols:
        sym = symbol_data['Symbol']
        share = db.execute("SELECT Shares FROM {} WHERE Symbol = ?".format(
            name[0]['username']), sym)
        price = lookup(sym)
        if price == None:
            return render_template("index.html")
        new_price = usd(price["price"])
        new_total = usd(price["price"] * float(share[0]["Shares"]))
        db.execute("UPDATE {} SET Price = ? WHERE Symbol = ?".format(
            name[0]['username']), new_price, sym)
        db.execute("UPDATE {} SET Total = ? WHERE Symbol = ?".format(
            name[0]['username']), new_total, sym)
    data = db.execute("SELECT * FROM {}".format(name[0]['username']))

    cash = db.execute("SELECT cash FROM users WHERE username = ?", name[0]['username'])
    return render_template("index.html", data=data, cash=usd(cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    STOCK = []

    if request.method == 'POST':
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Please type symbol", 400)
        share = request.form.get("shares")
        if not share or not str(share).isdigit() or int(share) <= 0:
            return apology("Shares must be a positive integer")
        check = lookup(symbol)
        share = int(share)

        if check is None:
            return apology("can't find symbol", 400)

        price = check.get("price")
        total = float(price * share)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if total > float(cash[0]['cash']):
            return apology("You don't have enough money")
        # time
        date_command_output = os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()
        date_part, time_part = date_command_output.split()
        year, month, day = map(int, date_part.split('-'))
        hour, minute, second = map(int, time_part.split(':'))
        # CASH
        cash = float(cash[0]['cash']) - float(total)

        symbol_own = db.execute("SELECT Symbol FROM {}".format(name[0]['username']))
        for data_symbol in symbol_own:
            STOCK.append(data_symbol["Symbol"])

        # update data
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        if symbol in STOCK:
            share_own = db.execute(
                "SELECT Shares FROM {} WHERE Symbol = ?".format(name[0]['username']), symbol)

            share_new = share + int(share_own[0]["Shares"])
            total_new = float(price) * float(share_new)
            db.execute("UPDATE {} SET Shares = ? WHERE Symbol = ?".format(
                name[0]['username']), share_new, symbol)
            db.execute("UPDATE {} SET Total = ? WHERE Symbol = ?".format(
                name[0]['username']), total_new, symbol)
        elif symbol not in STOCK:
            db.execute("INSERT INTO {} (Symbol,Name,Price,Shares,Total) VALUES (?,?,?,?,?)".format(
                name[0]['username']), symbol, symbol, price, share, total)
        db.execute("INSERT INTO {} (State,Symbol,Name,Shares,Price,DAY,MONTH,YEAR,HOUR,MINUTE) VALUES (?,?,?,?,?,?,?,?,?,?)".format(
            name[0]['username']+"history"), "BUY", symbol, symbol, share, price, day, month, year, hour, minute)
        flash(f"Bought {share} of {symbol} for {usd(total)}, Updated cash: {usd(cash)}")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    data = db.execute("SELECT * FROM {}".format(name[0]['username']+"history"))
    transaction = []
    for row in data:
        transaction.append([
            row["State"],
            row['Symbol'],
            row['Symbol'],
            row['Shares'],
            usd(float(row['Price'])),
            f"{row['MINUTE']}/{row['HOUR']} {row['DAY']}-{row['MONTH']}-{row['YEAR']}"
        ])
    return render_template("history.html", transaction=transaction)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        data_api = lookup(symbol)
        if data_api is not None:
            name = data_api.get("name")
            symbol_api = data_api.get("symbol")
            price = usd(data_api.get("price"))
            data = [name, symbol_api, price]
            for sheet in history_search:
                if name in sheet:
                    return render_template("quote.html", history_search=history_search)
            history_search.append(data)
        else:
            return apology("Can't find symbol")
        if name == None:
            return apology("Can't find symbol")
        if data_api == None:
            return apology("Can't find symbol")
        return render_template("quote.html", history_search=history_search)

    return render_template("quote.html")


@app.route("/deqoute", methods=["POST"])
def deregistrans():
    history_search.clear()
    return redirect('/quote')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        user_list = [row['username'] for row in db.execute("SELECT username FROM users")]
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check form error
        if not username:
            return apology("Please type your username")
        if username in user_list:
            return apology("Account has existed", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif password != confirmation:
            return apology("wrong confirm password")

        # UP DATA TO DATABASE
        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, hash)
        db.execute("CREATE TABLE ? (id INTEGER PRIMARY KEY AUTOINCREMENT, Symbol TEXT NOT NULL,Name TEXT NOT NULL,Price TEXT NOT NULL,Shares TEXT NOT NULL,Total TEXT NOT NULL)", username)
        db.execute("CREATE TABLE ? (id INTEGER PRIMARY KEY AUTOINCREMENT,State TEXT NOT NULL,Symbol TEXT NOT NULL,Name TEXT NOT NULL,Shares TEXT NOT NULL,Price TEXT NOT NULL,DAY TEXT NOT NULL,MONTH TEXT NOT NULL,YEAR TEXT NOT NULL,HOUR TEXT NOT NULL,MINUTE TEXT NOT NULL)", username + "history")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    STOCK = []
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    symbol_own = db.execute("SELECT Symbol FROM {}".format(name[0]['username']))
    for data_symbol in symbol_own:
        STOCK.append(data_symbol["Symbol"])
    if request.method == 'POST':
        symbol = request.form.get("symbol")
        share = request.form.get("shares")
        share_own = db.execute(
            "SELECT Shares FROM {} WHERE Symbol = ?".format(name[0]['username']), symbol)

        if not symbol:
            return apology("Please type symbol", 400)
        if not share or not str(share).isdigit() or int(share) <= 0:
            return apology("Shares must be a positive integer")
        share = int(share)
        if share > int(share_own[0]["Shares"]):
            return apology("Don't have enough share")
        check = lookup(symbol)

        if check == None:
            return apology("can't find symbol")

        price = check["price"]
        total = float(price) * float(share)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if total > float(cash[0]['cash']):
            return apology("You don't have enough money")
        # time
        date_command_output = os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()
        date_part, time_part = date_command_output.split()
        year, month, day = map(int, date_part.split('-'))
        hour, minute, second = map(int, time_part.split(':'))

        # CASH
        new_cash = float(cash[0]['cash']) + float(total)
        # share
        new_share = int(share_own[0]["Shares"]) - int(share)
        new_total = price * new_share

        if new_share == 0:
            db.execute("DELETE FROM {} WHERE Symbol = ?", symbol)
            STOCK.remove(symbol)
        elif new_share > 0:
            if symbol in STOCK:

                total_new = float(price) * float(new_share)
                db.execute("UPDATE {} SET Shares = ? WHERE Symbol = ?".format(
                    name[0]['username']), new_share, symbol)
                db.execute("UPDATE {} SET Total = ? WHERE Symbol = ?".format(
                    name[0]['username']), total_new, symbol)

        # update data
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        db.execute("INSERT INTO {} (State,Symbol,Name,Shares,Price,DAY,MONTH,YEAR,HOUR,MINUTE) VALUES (?,?,?,?,?,?,?,?,?,?)".format(
            name[0]['username']+"history"), "SELL", symbol, symbol, share, price, day, month, year, hour, minute)
        flash(f"Sell {new_share} of {symbol} for {usd(total)}, Updated cash: {usd(new_cash)}")
        return render_template("sell.html", stock=STOCK)
    return render_template("sell.html", stock=STOCK)
