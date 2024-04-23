# import libraries
import sqlite3
import secrets
import subprocess
from flask import Flask, redirect, render_template, request, flash, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

# configure app
app = Flask("__name__")
app.secret_key = secrets.token_bytes(24)

# configure session
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure db
database =  sqlite3.connect("main.db", check_same_thread=False)
conn = database.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# index
@app.route("/")
def index():
    if session.get("user_id"):
        conn.execute("SELECT username FROM users WHERE id = (?)", (session["user_id"],))
        username = conn.fetchone()[0]
        username = username[0].upper() + username[1:]
        return render_template("index.html", username=username)
    
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        if username == "" or password == "":
            return render_template("login.html")

        try:
            result = conn.execute("SELECT * FROM users WHERE username = (?)", (username,)).fetchone()

            if result == None:
                flash("Username not found")
                return render_template("login.html")
            
            else:
                hash = result[2]
                if check_password_hash(hash, password):
                    session["user_id"] = result[0]
                    flash("Login successful")
                    return redirect("/")
                
                else:
                    flash("Invalid password")
                    return render_template("login.html")

        except Exception as e:
            flash(str(e))
            return render_template("login.html")

    else:
        return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if username == "" or password == "" or (password != password2):
            flash("Invalid input")
            return render_template("register.html")
        
        elif len(password) < 4:
            flash("Password must be at least 4 characters long")
            return render_template("register.html")
        
        try:
            conn.execute("SELECT * FROM users WHERE username = (?)", (username,))
            
            if conn.fetchone() is not None:
                flash("Username already taken")
                return render_template("register.html")

            else:
                hash = generate_password_hash(password)
                conn.execute("INSERT INTO users (username, hash) VALUES (?,?)", (username, hash,))
                database.commit()
                conn.execute("SELECT last_insert_rowid()")
                session["user_id"] = conn.fetchone()[0]
                flash("Successfully registered")
                return redirect("/")
            
        except Exception as e:
            flash(str(e))
            return render_template("register.html")
    
    else:
        return render_template("register.html")

@app.route("/snippets", methods=["GET", "POST"])
def snippets():

    if request.method == "POST" and request.form.get(".method") == "delall":
        try:
            conn.execute("DELETE FROM snippets WHERE user_id = (?)", (session["user_id"],))
            database.commit()
            flash("All snippets deleted")
            return redirect("/snippets")
        
        except Exception as e:
            flash(str(e))
            return render_template("snippets.html")
        
    elif request.method == "POST" and request.form.get(".method") == "del":
        try:
            conn.execute("DELETE FROM snippets WHERE user_id = (?) AND id = (?)", (session["user_id"], request.form.get("snippet_id")))
            database.commit()
            flash("Snippet deleted")
            return redirect("/snippets")
        
        except Exception as e:
            flash(str(e))
            return render_template("snippets.html")
        
        
    elif request.method == "POST":
        title = request.form.get("title")
        code = request.form.get("code")

        if title == "" or code == "":
            flash("Invalid input")
            return render_template("snippets.html")
        
        code = code.replace("\n", "<br>")
        code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        
        try:
            conn.execute("INSERT INTO snippets (user_id, lang, code) VALUES (?,?,?)", (session["user_id"], title, code))
            database.commit()
            flash("Snippet added")
            return redirect(f"/{title.lower()}")
        
        except Exception as e:
            flash(str(e))
            return render_template("snippets.html")
        
    else:
        conn.execute("SELECT * FROM snippets WHERE user_id = (?)", (session["user_id"],))
        data = conn.fetchall()

        return render_template("snippets.html", details = data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# python
@app.route("/python", methods=["GET", "POST"])
def python():
    variables = {"title":"Python", "head":"Python", "action=":"/python"}

    if request.method == "POST":
        code = request.form.get("code")

        if code == "":
            flash("Null")
            return render_template("main.html", **variables)

        try:
            with open("temp/py_temp.py", "w") as f:
                f.write(code)

            process = subprocess.Popen(['python3', 'temp/py_temp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                output = stdout
                
            else:
                output = stderr
            
            return render_template("main.html", output = output, **variables)
        
        except Exception as e:
            return render_template("main.html", output = str(e), **variables)
        
    else:
        return render_template("main.html", **variables)
    
# C
@app.route("/c", methods=["GET", "POST"])
def c():
    variables = {"title":"C", "head":"C", "action=":"/c"}

    if request.method == "POST":
        code = request.form.get("code")

        if code == "":
            flash("Null")
            return render_template("main.html", **variables)
        
        try:
            with open("temp/c_temp.c", "w") as file:
                file.write(code)

            gcc = subprocess.run(['gcc', 'temp/c_temp.c', '-o', 'temp/c_temp'], capture_output=True)

            if gcc.returncode == 0:
                process = subprocess.Popen(['./temp/c_temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    output = stdout.decode()

                else:
                    output = stderr

            else:
                output = gcc.stderr.decode()

            return render_template("main.html", output = output, **variables)
        
        except Exception as e:
            return render_template("main.html", output = str(e), **variables)       
        
    else:
        return render_template("main.html", **variables)
    
# SQL
@app.route("/sql", methods=["GET", "POST"])
def sql():
    variables = {"title":"SQL", "head":"SQL", "action=":"/sql"}

    if request.method == "POST":
        code = request.form.get("code")

        if code == "":
            flash("Null")
            return render_template("main.html", **variables)
        
        try:
            subprocess.run(['sqlite3', 'temp/sql.db', '.exit'], check=True)

            process = subprocess.Popen(["sqlite3", "temp/sql.db"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=code)

            if process.returncode == 0:
                output = stdout

            else:
                output = stderr

            return render_template("main.html", output = output, **variables)
        
        except Exception as e:
            return render_template("main.html", output = str(e), **variables)
        
    else:
        return render_template("main.html", **variables)
    
    
if __name__ == "__main__":
    app.run(debug=True)
