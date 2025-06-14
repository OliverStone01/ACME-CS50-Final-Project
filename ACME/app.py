import random

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session

from functions import login_required, admin_required, gdp

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQlite database.
ACMEdb = SQL("sqlite:///acme.db")
userdb = SQL("sqlite:///redTeam.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Index function.
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Check if user has hacked the site.
    if session.get("hacked") != "valid":
        return render_template("index.html")
    else:
        return render_template("hackedIndex.html")


# Add customers to database.
@app.route("/addCustomer", methods=["POST"])
def addCustomer():
    if request.method == "POST":
        # check all data is submitted from form.
        if not request.form.get("company"):
            return render_template("dashboard.html", formMessage="Must provide the company name.")
        elif not request.form.get("firstName") or not request.form.get("secondName"):
            return render_template("dashboard.html", formMessage="Must provide Affiliates full name.")
        elif not request.form.get("package"):
            return render_template("dashboard.html", formMessage="Must select a valid package.")
        elif not request.form.get("days"):
            return render_template("dashboard.html", formMessage="Must provide length of contract.")
        else:
            # Set the data for database.
            company = request.form.get("company")
            firstName = request.form.get("firstName")
            secondName = request.form.get("secondName")
            affiliate = firstName + " " + secondName
            package = request.form.get("package")
            days = request.form.get("days")

        # Set the value of the package (Package value * days).
        if package == "Bronze":
            value = (50 * int(days))
        elif package == "Silver":
            value = (200 * int(days))
        elif package == "Gold":
            value = (500 * int(days))
        elif package == "Platinum":
            value = (1000 * int(days))
        else:
            return render_template("dashboard.html", formMessage="Must select a valid package")

        # Submit to database.
        ACMEdb.execute (
            "INSERT INTO customers (company, affiliate, package, days, value) VALUES(?, ?, ?, ?, ?)", company, affiliate, package, days, value
        )
        return redirect("/dashboard")


# If user gets caught, update users score in the database.
@app.route("/caught")
def caught():
    # Get users current caught count.
    caught = userdb.execute (
        "SELECT timesCaught FROM user"
    )
    # Add one to the current value.
    newValue = caught[0]["timesCaught"] + 1

    # Update the users count in the database.
    userdb.execute (
        "UPDATE user SET timesCaught = (?)", newValue
    )

    # Return json data.
    return jsonify({
        "caughtCount": newValue
    })


# Check if challenge one is complete.
@app.route("/challengeOne")
def challengeOne():
    # Check user database.
    user = userdb.execute (
        "SELECT * FROM user"
    )
    # if its not complete, update the user database to complete.
    if user[0]["challengeOne"] != 'complete':
        currentScore = user[0]["totalComplete"] + 1
        userdb.execute (
            "UPDATE user SET challengeOne = 'complete', totalComplete = ?", currentScore
        )

        # Display mission complete.
        return jsonify({
            "showMessage": True,
            "completeTitle": "Mission 1 Complete!",
            "completeText": "Congrats on completing the first hack! I know what you are thinking, that wasn't really much of a hack...But it's important to realise that if you don't want people getting access to certain parts of your website. then you need to remove all ways of access."
        })
    else:
        # If mission is already complete. return false.
        return jsonify({
            "showMessage": False
        })


# Check if challenge two is complete.
@app.route("/challengeTwo")
def challengeTwo():
    # Check user database.
    user = userdb.execute (
        "SELECT * FROM user"
    )
    # if its not complete, update the user database to complete.
    if user[0]["challengeTwo"] != 'complete':
        currentScore = user[0]["totalComplete"] + 1
        userdb.execute (
            "UPDATE user SET challengeTwo = 'complete', totalComplete = ?", currentScore
        )
        # Display mission complete.
        return jsonify({
            "showMessage": True
        })
    else:
        # If mission is already complete. return false.
        return jsonify({
            "showMessage": False
        })


# Check if challenge three is complete.
@app.route("/challengeThree")
def challengeThree():
    # Check user database to see if mission is already complete.
    user = userdb.execute (
        "SELECT * FROM user"
    )
    # if challenge three is not complete, update the user database to "complete".
    if user[0]["challengeThree"] != "complete":
        currentScore = user[0]["totalComplete"] + 1
        userdb.execute (
            "UPDATE user SET challengeThree = 'complete', totalComplete = ?", currentScore
        )
        #Display mission Complete.
        return jsonify({
            "showMessage": True
        })
    else:
        # Else if mission is already complete, return false.
        return jsonify({
            "showMessage": False
        })


# Check if challenge four is complete.
@app.route("/challengeFour", methods=["POST"])
def challengeFour():
    if request.method == "POST":
        if request.form.get("search") == "eggFoundACME":
            user = userdb.execute (
                "SELECT * FROM user"
            )
            if user[0]["challengeFour"] != "complete":
                currentScore = user[0]["totalComplete"] + 1
                userdb.execute (
                    "UPDATE user SET challengeFour = 'complete', totalComplete = ?", currentScore
                )
                session["egg"] = "complete"
                #Display mission Complete.
                if session["hacked"] == "valid":
                    return render_template("hackedIndex.html", eggComplete=True)
                else:
                    return render_template("index.html", eggComplete=True)
            else:
                # Else if mission is already complete, return false.
                return redirect("/")
        else:
            return redirect("/")


# Admin Dashboard.
@app.route("/dashboard")
@login_required
@admin_required
def dashboard():
    # Get all data for the dashboard.
    customers = ACMEdb.execute (
        "SELECT * FROM customers;"
    )
    total = ACMEdb.execute (
        "SELECT COUNT(*) FROM customers"
    )
    profit = ACMEdb.execute (
        "SELECT SUM(value) FROM customers"
    )

    # Randomise task amount.
    tasks = total[0]["COUNT(*)"] * (random.randrange(2,5))

    return render_template("dashboard.html", tasks=tasks, totalProfit=(gdp(profit[0]["SUM(value)"])), customers=customers, totalCustomers=total[0]["COUNT(*)"])


# Edit website.
@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        # Check if the correct keyword has been used.
        if request.form.get("keyword") == "Deface":
            session["hacked"] = "valid"
            # Check user database.
            user = userdb.execute (
                "SELECT * FROM user"
            )
            return render_template("hackedIndex.html")

        elif request.form.get("keyword") == "Default":
            return render_template("index.html")
        else:
            return render_template("dashboard.html", message="Incorrect Keyword")


# Check if all challenges are complete.
@app.route("/finalCheck")
def finalCheck():
    # Check user database to see if all challenges have been complete.
    user = userdb.execute (
        "SELECT * FROM user"
    )
    if user[0]["challengeOne"] == "complete" and user[0]["challengeTwo"] == "complete" and user[0]["challengeThree"] == "complete" and user[0]["challengeFour"] == "complete":
        return jsonify({"complete": True})


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    # User submits login.
    if request.method == "POST":
        # Check if username was submited.
        if not request.form.get("username"):
            return render_template("login.html", errorMessage="Must provide a username")

        # Check if password was submited.
        elif not request.form.get("password"):
            return render_template("login.html", errorMessage="Invalid Password")


        # The following code in prone to SQL injection (First Challenge).
        username = request.form.get("username")
        password = request.form.get("password")

        # Check the database for username and password.
        check = ACMEdb.execute(
            "SELECT * FROM users WHERE username = '%s'  AND password = '%s'" % (username, password)
        )

        # Return error if the login is incorrect.
        if not check:
            return render_template("login.html", errorMessage="Invalid Username/Password")

        # else login and remeber the user_id in session.
        else:
            # Remeber which user has logged in.
            session["user_id"] = check[0]["id"]

            # Redirect to dashboard.
            return redirect("/dashboard")

    else:
        return render_template("login.html")


# Logout user by clearing the sessions and log back into the original user.
@app.route("/logout")
def logout():
    if session.get("hacked") == "valid":
        session.clear()
        user = userdb.execute (
            "SELECT * FROM user"
        )
        session["user_id"] = user[0]["id"]
        session["hacked"] = "valid"
    else:
        session.clear()
        user = userdb.execute (
            "SELECT * FROM user"
        )
        session["user_id"] = user[0]["id"]
    return redirect("/")


# Mission control to display current mission, times caught, hint, and answer.
@app.route("/missionControl")
def missionControl():
    # Get data from user.
    user = userdb.execute (
        "SELECT * FROM user"
    )

    # Check if the mission is complete. If it's not, then that's the current mission.
    if user[0]["challengeOne"] != 'complete':
        question = "- Find the hidden employee login page."
        questionHint = "- This challenge doesn't need hacking - just pay close attention to the entire homepage... or think like a URL."
        questionAnswer = "- There is an 'Employee Login' link in the footer of the page. Also, you can do '/login' in the URL to gain access."

    elif user[0]["challengeTwo"] != 'complete':
        question = "- Get access to the Admin's account."
        questionHint = "- Someone left a sticky note here... shame the password's covered. Maybe we don't need it - do you think a little injection will do..."
        questionAnswer = "- SQL injection - Password = ' OR '1'='1"

    elif user[0]["challengeThree"] != 'complete':
        question = "- Find the website editor on the admin's dashboard and deface the site!"
        questionHint = "- IT have made it really clear what not to type. it'd be a shame if someone... typed it anyway."
        questionAnswer = "- Type 'Deface' into the admins 'edit homepage' input bar."

    elif user[0]["challengeFour"] != 'complete':
        question = "- Congrats on completing the main challenges, but can you find the Easter egg...?"
        questionHint = "- If you had access to the admin panel, where would you hide a secret? Maybe under the hood..."
        questionAnswer = "- Use inspection tools on the Admins homepage and look for a large egg with a code inside. Input this code in the Admins search bar."

    else:
        question = "- Your all done! Well done on completing all the challenges!"
        questionHint = "- No Hints left!"
        questionAnswer = "- No Answers left!"

    # Return json data back to mission control.
    return jsonify({
        "timesCaught": user[0]["timesCaught"],
        "totalComplete": user[0]["totalComplete"],
        "question": question,
        "hint": questionHint,
        "answer": questionAnswer
    })


# Reset site and data.
@app.route("/reset", methods=["POST"])
def reset():
    session.pop("user_id", None)
    session.clear()
    login_required
    return jsonify({"success": True})


