# import libraries
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

#c onfigure app
app = Flask("__name__")
app.run(debug=True)

# configure session
app.config["SESSION_PERMANANT"] = True
app.config["SESSION_TYPE"] = "signed_cookies"
Session(app)

# configure db
db = sqlite3.connect("details.db")
cursor = db.cursor()

# index 
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        code = request.form.get("code")
        if not code:
            return redirect("/")
        
        return redirect("/")
    else:
        return render_template("index.html")
    