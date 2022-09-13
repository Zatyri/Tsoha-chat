from app import app
from flask import render_template, session, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():        
    if 'username' in session:
        id_token = session['username']        
    return render_template("index.html")

@app.route('/login',methods=["POST"])
def login():
    if 'username' in session:
        del session['username']
    username = request.form['username']
    password = request.form['password']
    hash_value = generate_password_hash(password)

    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html") 

@app.route("/register/me" , methods=["POST"])
def registerMe():
    username = request.form['username']
    password = request.form['password']
    passwordVerification = request.form['passwordVerification']
    return redirect("/")