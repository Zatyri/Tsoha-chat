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
    sql = """SELECT DISTINCT ON (messages.id) messages.id, rooms.title, rooms.isPrivate, messages.content, messages.likes, messages.postedTime, users.username
          FROM rooms, users, messagesinroom
          LEFT JOIN messages ON messages.id = messagesinroom.messageid
          WHERE messagesinroom.room = (:roomID)"""

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
    sqlAddUserToRoom = "INSERT INTO usersInRoom (room, userID) VALUES (:room, :userID)"
    db.session.execute(sqlAddUserToRoom, {"room": roomID, "userID": userID})

    db.session.commit() 
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
    
