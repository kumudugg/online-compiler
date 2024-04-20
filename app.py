#import libraries
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

#configure app
app = Flask("__name__")

#configure session
app.config["SESSION_PERMANANT"] = True
app.config["SESSION_TYPE"] = "signed_cookies"
Session(app)

# configure db
db = sqlite3.connect("details.db")
cursor = db.cursor()

# index 
@app.route("/")
def index():
    return render_template("layout.html")
    