from app import app
from flask import render_template, session, request, redirect
from werkzeug.security import generate_password_hash
from models import User
from services.auth import addUser, checkIfUserExists, userLogin


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
    
    if not userLogin(username, password):        
        return redirect("/")
    
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
    if checkIfUserExists(username):
        return redirect("/register")
    
    password = request.form['password']
    passwordVerification = request.form['passwordVerification']
    
    if password != passwordVerification:
        return redirect("/register")

    hash_value = generate_password_hash(password)
    user = User(username, hash_value)

    addUser(user)
    
    return redirect("/")