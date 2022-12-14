import secrets
from app import app
from flask import abort, render_template, session, request, redirect
from werkzeug.security import generate_password_hash
from models import User
from services.auth import addUser, changePassword, checkIfUserExists, checkUsersPassword, deleteUser, userLogin
from services.messageService import addMessage, addUserToPrivateRoom, checkUserAccessToRoom, getRoomAdmin, getUsersInRoom, createNewRoom, getMessagesInRoom, getRoomTitle, getUsersRooms, getIsRoomPrivate, likeMessage, removeUserFromRoom


@app.route("/")
def index():
    rooms = []    
    messages = []
    userID = -1
    roomID = "1"
    userHasAccess = False
    error = None
    userInput = ""

    if 'csrf_token' not in session:
        session["csrf_token"] = secrets.token_hex(16)

    if 'username' in session:
        id_token = session['username']
        messages = getMessagesInRoom()

    if 'userInput' in session:
        userInput = session["userInput"]
        del session["userInput"]

    if request.args.get('room'):           
        roomID = request.args.get('room')
    
    session["activeRoom"] = roomID
        
    if 'userID' in session:
        userID = session['userID']
        rooms = getUsersRooms(userID)

    if 'error' in session:
        error = session['error']
        del session['error']

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

    return render_template("index.html", messages=messages, rooms=rooms, title=title, isPrivate=isPrivate, nonMembers=nonMembers, members=members , userHasAccess=userHasAccess, error=error, input=userInput)

@app.route("/postMessage", methods=["POST"])
def postMessage():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    messageContent = request.form['messageContent']
    userID = session['userID']
    roomID = session["activeRoom"]

    if checkUserAccessToRoom(roomID, userID):
        session['error'] = "Sinulla ei ole pääsyä huoneeseen"
    else:
        addMessage(roomID, userID, messageContent)

    return redirect("/?room=" + roomID)

@app.route('/login',methods=["POST"])
def login():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if 'username' in session:
        del session["username"]
    if 'userID' in session:
        del session['userID']
    username = request.form['username']
    password = request.form['password']
    
    userID = userLogin(username, password)
    if not userID > 0:
        session["userInput"] = username
        session['error'] = "Väärä käyttäjätunnus tai salasana"    
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
    if 'csrf_token' in session: 
        del session["csrf_token"]
    return redirect("/")

@app.route("/register")
def register():
    error = None
    userInput = ""
    if 'userInput' in session:
        userInput = session["userInput"]
        del session["userInput"]
    if 'error' in session:        
        error = session['error']
        del session['error']

    return render_template("register.html", error=error, input=userInput) 

@app.route("/register/me", methods=["POST"])
def registerMe():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = request.form['username']
    if checkIfUserExists(username):
        session["userInput"] = username
        session['error'] = "Käyttäjänimi on varattu, valitse toinen käyttäjänimi"
        return redirect("/register")
    
    password = request.form['password']
    passwordVerification = request.form['passwordVerification']
    
    if password != passwordVerification:
        session['error'] = "Salasanat eivät täsmää"
        return redirect("/register")

    hash_value = generate_password_hash(password)
    user = User(username, hash_value)

    addUser(user)
    
    return redirect("/")

@app.route("/createRoom", methods=["POST"])
def createRoom():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    userID = session['userID']
        
    isPrivate = request.form.get('isPrivate')
    
    roomName = request.form['roomName']

    roomID = createNewRoom(userID, isPrivate, roomName)
    session["activeRoom"] = roomID


    return redirect("/?room=" + str(roomID))

@app.route("/inviteUser", methods=["POST"])
def inviteUser():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
        session['error'] = "Huoneen pääkäyttäjää ei voida poistaa"
        return redirect("/?room=" + str(roomID)) 
    removeUserFromRoom(userToRemove, roomID)

    return redirect("/?room=" + str(roomID))

@app.route("/account")
def account():
    if not "userID" in session:
        return redirect("/")
    
    error = None

    if "error" in session:
        error = session['error']
        del session['error']

    return render_template("account.html", error=error)

@app.route("/deleteMe")
def deleteMe():
    if not "userID" in session:
        del session["csrf_token"]
        return redirect("/")    
    
    deleteUser(session['userID'])
    session.clear()
    return redirect("/")

@app.route("/changePassword", methods=["POST"])
def updatePassword():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    userID = session['userID']        
    currentPassword = request.form['currentPassword']

    if not checkUsersPassword(userID, currentPassword):
        session['error'] = "Nykyinen salasana meni väärin"
        return redirect("/account")
    
    password = request.form['newPassword']
    passwordVerification = request.form['newPasswordVerification']
    
    if password != passwordVerification:
        session['error'] = "Salasanat eivät täsmää"
        return redirect("/account")

    changePassword(userID, password)

    return redirect("/account")

@app.route("/like/", )
def likeMsq():

    userID = session['userID']   
    roomID = session["activeRoom"]   
    if checkUserAccessToRoom(roomID, userID):
        return redirect("/?room=" + str(roomID))
    
    messageToLike = request.args.get('message')

    if not likeMessage(messageToLike, userID):        
        session['error'] = "Et voi tykätä samasta viestistä kuin kerran"

    return redirect("/?room=" + str(roomID))

@app.route("/postReply", methods=["POST"])
def postReply():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    messageContent = request.form['messageContent']
    parentMessage = int(request.form['parent'])
    userID = session['userID']
    roomID = session["activeRoom"]

    if checkUserAccessToRoom(roomID, userID):
        session['error'] = "Sinulla ei ole pääsyä huoneeseen"
    else:
        addMessage(roomID, userID, messageContent, parentMessage)    

    return redirect("/?room=" + roomID)

