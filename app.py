# import libraries
import os
import subprocess
from flask import Flask, redirect, render_template, request

# configure app
app = Flask("__name__")

# index
@app.route("/")
def index():
    return render_template("index.html")

# python
@app.route("/python", methods=["GET", "POST"])
def python():
    if request.method == "POST":

        code = request.form.get("code")

        if code == "":
            return render_template("python.html")

        try:
            process = subprocess.Popen(['python3', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                output = stdout

            else:
                output = stderr
            
            return render_template("python.html", output = output)
        
        except Exception as e:
            return render_template("python.html", output = str(e))
        
    else:
        return render_template("python.html")
    

@app.route("/c", methods=["GET", "POST"])
def c():
    if request.method == "POST":

        code = request.form.get("code")

        if code == "":
            return render_template("c.html")
        
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


            return render_template("c.html", output = output)
        
        except Exception as e:
            return render_template("c.html", output = str(e))       
        
    else:
        return render_template("c.html")
    

        
