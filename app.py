# import libraries
import sqlite3
import subprocess
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

#c onfigure app
app = Flask("__name__")

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

        try:
            process = subprocess.Popen(['python3', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                output = stdout

            else:
                output = stderr
            
            return render_template("index.html", output = output)
        
        except Exception as e:
            return render_template("index.html", error = str(e))
        
    else:
        return render_template("index.html")
    