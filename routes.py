from app import app
from flask import render_template, session, request, redirect
from werkzeug.security import generate_password_hash
from models import User
from services.auth import addUser, checkIfUserExists, userLogin
from services.messageService import addMessage, createNewRoom, getMessagesInRoom


@app.route("/")
def index():        
    if 'username' in session:
        id_token = session['username']
        messages = getMessagesInRoom()
    if 'activeRoom' not in session:
        session["activeRoom"] = 1

    messages = getMessagesInRoom(session["activeRoom"])
    return render_template("index.html", messages=messages)

@app.route("/postMessage", methods=["POST"])
def postMessage():
    messageContent = request.form['messageContent']
    userID = session['userID']
    roomID = session["activeRoom"]

    addMessage(roomID, userID, messageContent)

    return redirect("/")

@app.route('/login',methods=["POST"])
def login():
    if 'username' in session:
        del session["username"]
    if 'userID' in session:
        del session['userID']
    username = request.form['username']
    password = request.form['password']
    
    userID = userLogin(username, password)
    if not userID > 0:        
        return redirect("/")
    
    session["username"] = username  
    session['userID'] = userID  
    return redirect("/")

@app.route("/logout")
def logout():
    if 'username' in session:
        del session["username"]
    if 'userID' in session:
        del session['userID']
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html") 

@app.route("/register/me", methods=["POST"])
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

@app.route("/createRoom", methods=["POST"])
def createRoom():
    userID = session['userID']
        
    isPrivate = request.form.get('isPrivate')
    
    roomName = request.form['roomName']

    createNewRoom(userID, isPrivate, roomName)

    return redirect("/")