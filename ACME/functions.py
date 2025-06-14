import random

from cs50 import SQL
from flask import render_template, session
from functools import wraps

# Set user database.
userdb = SQL("sqlite:///redTeam.db")

# login function that forces the user to login to certain places of the site.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        # if session doesn't have a user, clear the database, set username to a random number, and insert into database.
        if session.get("user_id") is None:
            userdb.execute (
                "DELETE FROM user"
            )
            session["user_id"] = random.randrange(2,100)
            session["hacked"] = "invalid"
            userdb.execute (
                "INSERT INTO user (id, timesCaught, totalComplete) VALUES(?, '0', '0')", session["user_id"]
            )
            return render_template("/index.html", new=True)
        return f(*args, **kwargs)

    return decorated_function


# Function to check if the user is admin, if not, send user to login page.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") !=1:
            return render_template("/login.html")
        return f(*args, **kwargs)

    return decorated_function


# Function for changing value into GDP.
def gdp(value):
    """Format value as GDP."""
    return f"{value:,.2f}"
