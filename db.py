from app import app
from flask_sqlalchemy import SQLAlchemy
from models import User
import os

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def checkIfUserExcistsinDatabase(username: str) -> bool:
  try:
    sql = "SELECT EXISTS (SELECT * FROM users WHERE users.username = (:username))"
    result = db.session.execute(sql, {"username":username})   
      
    return result.first()[0]    
  except: 
    return False
    
def addUserToDatabase(user: User) -> bool:
  try:
    sql = "INSERT INTO users (username, password, uuid) VALUES (:username, :password, :uuid)"
    db.session.execute(sql, {"username":user.username, "password":user.password, "uuid":user.uuid})
    db.session.commit()
    return True
  except:
    return False

def getUsersPasswordAndID(username: str):
  try:    
    sql = "SELECT id, password FROM users WHERE users.username = (:username)"
    result = db.session.execute(sql, {"username":username})
    return result.first()    
  except Exception as e: print(e)
    
def getMessagesInRoomFromDB(roomID:int):  
  try:    
    sql = """SELECT messages.id, rooms.title, rooms.isPrivate, messages.content, messages.postedTime, users.username
          FROM messages
          LEFT JOIN messagesinroom ON messagesinroom.messageid = messages.id
          LEFT JOIN users ON messages.author = users.id
          LEFT JOIN rooms ON rooms.id = messagesinroom.room
          WHERE messagesinroom.room = (:roomID)
          ORDER BY messages.postedTime"""

    result = db.session.execute(sql, {"roomID":roomID})         
    return result.fetchall()  
  except Exception as e: print(e)

def addMessageToDB(roomID:int, author:int, content:str, postedTime:str):
  try:    
    sqlAddMessage = "INSERT INTO messages (author, content, postedTime) VALUES (:author, :content, :postedTime) RETURNING id"
    result = db.session.execute(sqlAddMessage, {"author":author, "content":content, "postedTime":postedTime})
    messageID = result.first()[0]

    sqlAddRelation = "INSERT INTO messagesInRoom (room, messageID) VALUES (:room, :messagesID)"
    db.session.execute(sqlAddRelation, {"room":roomID, "messagesID":messageID}) 

    db.session.commit() 

  except Exception as e: print(e)

def createRoomToDB(userID:int, isPrivate:bool, roomName:str) -> int:
  try:    
    sql = "INSERT INTO rooms (title, creator, isPrivate) VALUES (:title, :creator, :isPrivate) RETURNING id"
    result = db.session.execute(sql, {"title":roomName, "creator":userID, "isPrivate":isPrivate})
    roomID = result.first()[0]
    db.session.commit() 
    addUserToRoomInDB(userID, roomID)

    return roomID
  except Exception as e: print(e)

def getUsersRoomsfromDB(userID:int) -> int:
  try:    
    sql = """SELECT r.id as roomID, r.title as roomTitle, r.isPrivate as isPrivate, r.creator as creator 
            FROM rooms as r LEFT JOIN usersinroom ON usersinroom.room = r.id
            WHERE usersinroom.userid = (:userID) OR r.isprivate = false"""
    result = db.session.execute(sql, {"userID":userID})    

    return result.fetchall()  
  except Exception as e: print(e)

def getUserInRoom(roomID: int, userID:int):
  try:    
    sql = "SELECT u.userID FROM usersInRoom as u WHERE u.room = (:roomID) AND u.userID = (:userID) GROUP BY u.userID"

    result = db.session.execute(sql, {"roomID": roomID, "userID":userID})    

    return result.fetchall()  
  except Exception as e: print(e)

def getRoomIsPrivate(roomID: int):
  try:    
    sql = "SELECT u.isPrivate FROM rooms as u WHERE u.id = (:roomID)"

    result = db.session.execute(sql, {"roomID": roomID})    

    return result.fetchall()[0][0]
  except Exception as e: print(e)

def getRoomTitleFromDB(roomID: int):
    try:    
      sql = "SELECT u.title FROM rooms as u WHERE u.id = (:roomID)"

      result = db.session.execute(sql, {"roomID": roomID})    

      return result.fetchall()[0][0]
    except Exception as e: print(e)

def getIsRoomInfo(roomID:int):
  try:    
    sql = "SELECT r.id, r.title, r.creator, r.isPrivate FROM rooms as r WHERE r.id = (:roomID)"

    result = db.session.execute(sql, {"roomID": roomID})    

    return result.fetchall()[0]
  except Exception as e: print(e)

def getUsersNotInRoomFromDB(roomID:int):
  try:    
    sql = """SELECT u.id, u.username FROM users as u
          WHERE NOT EXISTS(SELECT * FROM usersinroom 
          WHERE usersinroom.room = (:roomID) AND usersinroom.userID = u.id )"""

    result = db.session.execute(sql, {"roomID": roomID})    

    return result.fetchall()
  except Exception as e: print(e)

def addUserToRoomInDB(userID: int, roomID: int):
  try:    
    sql = "INSERT INTO usersInRoom (room, userID) VALUES (:room, :userID)"
    db.session.execute(sql, {"room": roomID, "userID": userID})

    db.session.commit() 
  except Exception as e: print(e)

def getUsersInRoomFromDB(roomID:int):
  try:    
    sql = """SELECT u.id, u.username FROM users as u
          WHERE EXISTS(SELECT * FROM usersinroom 
          WHERE usersinroom.room = (:roomID) AND usersinroom.userID = u.id)"""

    result = db.session.execute(sql, {"roomID": roomID})    

    return result.fetchall()
  except Exception as e: print(e)

def removeUserFromRoomInDB(userID: int, roomID: int):
  try:    
    sql = "DELETE FROM usersInRoom WHERE userID = (:userID) AND room = (:roomID)"
    db.session.execute(sql, {"roomID": roomID, "userID": userID})    
    db.session.commit() 
  except Exception as e: print(e)

def deleteUserFromDB(userID: int):
  try:    
    sql = "DELETE FROM users WHERE id = (:userID)"
    db.session.execute(sql, {"userID": userID})    
    db.session.commit() 
  except Exception as e: print(e)

def getUsersPassword(userID: int):
  try:    
    sql = "SELECT password FROM users WHERE users.id = (:userID)"
    result = db.session.execute(sql, {"userID":userID})
    return result.first()[0]
  except Exception as e: print(e)

def updateUsersPassword(userID: int, newPassword: str):
  try:    
    sql = "UPDATE users SET password = (:newPassword) WHERE id = (:userID)"
    db.session.execute(sql, {"userID":userID, "newPassword": newPassword})
    db.session.commit() 
  except Exception as e: print(e)

def addLikeToMessageInDB(msgID: int, userID:int):
  try:    
    sql = "INSERT INTO likedMessages (messageID, userID) VALUES (:msgID, :userID)"
    db.session.execute(sql, {"msgID": msgID, "userID": userID})
    db.session.commit() 
  except Exception as e: print(e)

def checkIfUserLikedMessage(msgID: int, userID: int):
  try:    
    sql = "SELECT * FROM likedMessages WHERE userID = (:userID) AND messageID = (:msgID)"
    result = db.session.execute(sql, {"msgID": msgID, "userID": userID})
    return result.first()
  except Exception as e: print(e)

def countMessageLikes(msgID: int):
  try:    
    sql = "SELECT COUNT(*) FROM likedMessages WHERE messageID = (:msgID)"
    result = db.session.execute(sql, {"msgID": msgID})    
    return result.first()[0]
  except Exception as e: print(e)

def addReplyToDB(roomID:int, author:int, content:str, postedTime:str, parentMessage:int):
  try:    
    sqlAddMessage = "INSERT INTO messages (author, content, postedTime) VALUES (:author, :content, :postedTime) RETURNING id"
    result = db.session.execute(sqlAddMessage, {"author":author, "content":content, "postedTime":postedTime})
    messageID = result.first()[0]

    sqlAddRelation = "INSERT INTO repliedMessages (parentMessage, childMessage) VALUES (:parentMessage, :messagesID)"
    db.session.execute(sqlAddRelation, {"parentMessage":parentMessage, "messagesID":messageID}) 

    db.session.commit() 

  except Exception as e: print(e)

def getRepliesFromDB(msgID: int):
  try:    
    sql = """SELECT messages.id, users.username, messages.content, messages.postedTime 
          FROM messages
          LEFT JOIN repliedMessages ON repliedMessages.childMessage = messages.id
          LEFT JOIN users ON messages.author = users.id
          WHERE repliedMessages.parentMessage = (:msgID)
          ORDER BY messages.postedTime"""

    result = db.session.execute(sql, {"msgID":msgID})         
    return result.fetchall()  
  except Exception as e: print(e)