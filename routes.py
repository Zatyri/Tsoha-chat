from app import app
from flask import render_template, session, request, redirect
from werkzeug.security import generate_password_hash
from models import User
from services.auth import addUser, checkIfUserExists, userLogin
from services.messageService import addMessage, addUserToPrivateRoom, checkUserAccessToRoom, getRoomAdmin, getUsersInRoom, createNewRoom, getMessagesInRoom, getRoomTitle, getUsersRooms, getIsRoomPrivate, removeUserFromRoom


@app.route("/")
def index():
    rooms = []    
    messages = []
    userID = -1
    roomID = "1"
    userHasAccess = False
    if 'username' in session:
        id_token = session['username']
        messages = getMessagesInRoom()

    if request.args.get('room'):           
        roomID = request.args.get('room')
    
    session["activeRoom"] = roomID
        
    if 'userID' in session:
        userID = session['userID']
        rooms = getUsersRooms(userID)

    messages = getMessagesInRoom(session["activeRoom"], userID)
    title = getRoomTitle(session["activeRoom"], userID)
    isPrivate = getIsRoomPrivate(session["activeRoom"])

    nonMembers = []
    members = []
    if isPrivate:
        nonMembers = getUsersInRoom(session["activeRoom"], True)    
        members = getUsersInRoom(session["activeRoom"]) 
    
    if title == None:
        title = "johon sinulla ei ole pääsyä"
    else:
        userHasAccess = True

    return render_template("index.html", messages=messages, rooms = rooms, title=title, isPrivate=isPrivate, nonMembers=nonMembers, members=members , userHasAccess=userHasAccess)

@app.route("/postMessage", methods=["POST"])
def postMessage():
    messageContent = request.form['messageContent']
    userID = session['userID']
    roomID = session["activeRoom"]

    addMessage(roomID, userID, messageContent)

    return redirect("/?room=" + roomID)

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
    if 'activeRoom' in session:
        del session["activeRoom"]
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

    roomID = createNewRoom(userID, isPrivate, roomName)
    session["activeRoom"] = roomID


    return redirect("/?room=" + str(roomID))

@app.route("/inviteUser", methods=["POST"])
def inviteUser():

    userID = session['userID']        
    roomID = session["activeRoom"]

    if checkUserAccessToRoom(roomID, userID):
        return redirect("/?room=" + str(roomID))
    
    userToAdd = request.form.get('inviteUsers')

    addUserToPrivateRoom(userToAdd, roomID)

    return redirect("/?room=" + str(roomID))

@app.route("/removeUserFromRoom/",)
def removeUser():

    userID = session['userID']        
    roomID = session["activeRoom"]
    
    userToRemove = request.args.get('user')
    roomAdmin = getRoomAdmin(roomID)

    if int(userToRemove) == roomAdmin :
        return redirect("/?room=" + str(roomID)) 
    removeUserFromRoom(userToRemove, roomID)

    return redirect("/?room=" + str(roomID))