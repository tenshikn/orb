import sys
import os
import sqlite3
import requests
import base64
import datetime
import random

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, wiki_search, usd

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

# Database configurations

# Connect sqlite3 to database
# Share connection with multiple threads and enable autocommit
connection = sqlite3.connect("ithou.db", check_same_thread=False, isolation_level=None)

# Setting row_factory property of connection object to use sqlite3's implementation
connection.row_factory = sqlite3.Row

# Creating cursor object to enable databasae executions
db = connection.cursor()

@app.route('/', methods=['GET', 'POST'])
@app.route("/login", methods=["GET", "POST"])
def index():
    # clear all sessions
    session.clear()

    # render index.html if page was gotten by url or redirect
    if request.method == 'GET':
        return render_template("index.html")

    # Elif request method is POST (a form is submitted)
    # Get username submitted
    username = request.form.get('username')

    # Get password submitted
    password = request.form.get('password')

    # Enusre Username and Password field where filled
    if not username:
        return apology("No Username Entered")
    elif not password:
        return apology("Password Needed to Login")

    # Query database for username and crosscheck entered password with hashed password
    else:
        db.execute("SELECT * FROM users WHERE username=?", (username,))

        # Create list of rows queried
        rows = [dict(row) for row in db.fetchall()]
        if len(rows) == 0 or not check_password_hash(rows[0]['password_hash'], password):
            return apology("Invalid Username or Password")
        else:
            # Store user's id and username in session
            session['user_id'], session["username"] = rows[0]['id'], rows[0]['username']
            return redirect('/home')

# Route for AJAX call

@app.route('/signing')
def signing():
    return jsonify(render_template('signup.html'))


@app.route('/register', methods=["GET", "POST"])
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return redirect('/')
    elif request.method == "POST":
        # Retrieve input values
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('password_confirm')

        # Validation
        if not first or not last:
            return apology("Your name is needed to create an account")
        if not username:
            return apology("No username set")
        if not email:
            return apology("No email address entered")
        if not password or not confirmation:
            return apology("Ensure both password fields are entered")
        if password != confirmation:
            return apology("Passwords do not match")

        # Ensure email address is unique
        db.execute("SELECT * FROM users WHERE email=?", (email,))
        rows = [dict(row) for row in db.fetchall()]
        if len(rows) != 0:
            return apology("DON'T BE STUPID. ENTER YOUR UNIQUE EMAIL")

        # Hash user's password for database storage
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=10)

        # Check if username already exists and create new username if so
        db.execute("SELECT * FROM users WHERE username=?", (username,))
        rows = [dict(row) for row in db.fetchall()]
        if len(rows) != 0:
            username += str((rows[-1]['id'] + 1))
        print(username)
        # Insert new user into database
        db.execute("INSERT INTO users (username, first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?, ?)",
                   (username, first, last, email, password_hash))
        flash("SIGNED!")
        return render_template("index.html")



@app.route('/new-topic', methods=["GET", "POST"])
@login_required
def new_topic():
    # Visiting route via link
    if request.method == "GET":
        return render_template("new-topic.html")
    # Post request: User submits title and/or entry
    else:
        image_url = request.form.get('image_url')
        title = request.form.get('title')
        entry_heading = request.form.get('entry_heading')
        entry = request.form.get('entry')
        # Get image from url
        try:
            response_image = requests.get(image_url)
            response_image.raise_for_status()
            image = response_image.content
        except requests.RequestException:
            image = None

        # Add info to vault table
        if title:
            db.execute("INSERT INTO vault (user_id, title, photo, date_added) VALUES (?, ?, ?, (SELECT datetime('now')))",
            (session["user_id"], title, image))

            # Add info to entry table if any
            if entry:
                if not entry_heading:
                    return apology("Your entry needs a heading, try to think of something simple!", 400)
                else:
                    db.execute("INSERT INTO entries(user_id, title, entry_heading, entry, date_added) VALUES (?, ?, ?, ?, (SELECT datetime('now')))",
                    (session['user_id'], title, entry_heading, entry))

        return redirect('/home')
















@app.route('/_title-search', methods=['POST'])
@login_required
def title_search():
    if request.method == "POST":
        title = request.form.get("title")
        print("Title being searched: ",title)
        print("title data type: ", type(title))
        print("FROM WIKI SEARCH", wiki_search(title))
        return jsonify(wiki_search(title))




@app.route('/home')
@login_required
def home():
    db.execute("SELECT photo, title, date_added FROM vault WHERE user_id=? GROUP BY title", (session["user_id"], ))
    rows = [dict(row) for row in db.fetchall()]
    if len(rows) == 0:
        data="Nothing to show here yet"
    else:
        data = dict()
        for row in rows:
            data[row['title']] = base64.b64encode(row['photo']).decode('utf-8') if row['photo'] is not None else row['title']

    #print(data['Gum gum fruit'])
    #random.shuffle(data)

    return render_template('home.html', data=data)





























@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")





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
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
