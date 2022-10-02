from datetime import datetime

from models import Message, Room, SimpleUser
from db import addMessageToDB, addUserToRoomInDB, getIsRoomInfo, getUsersInRoomFromDB,getUsersNotInRoomFromDB, createRoomToDB, getMessagesInRoomFromDB, getRoomIsPrivate, getRoomTitleFromDB, getUsersRoomsfromDB, getUserInRoom, removeUserFromRoomInDB


def getMessagesInRoom(roomID: int=1, userID: int = None):
  if userID is None:
    return []
  if checkUserAccessToRoom(roomID, userID):    
    return []

  messagesResult = getMessagesInRoomFromDB(roomID)
  messageArray =  []
  
  if messagesResult == None:
    return []

  for msg in messagesResult:    
    messageArray.append(Message(msg[0], msg[6], roomID, msg[3], msg[4], msg[5], msg[1], msg[2]))
  
  return list(reversed(messageArray))

def checkUserAccessToRoom(roomID: int, userID: int):
  isPrivate = getRoomIsPrivate(roomID)  
  if isPrivate:
    result = getUserInRoom(roomID, userID) 
    if len(result) > 0 and result[0][0] == userID:  
      return False
    return True
  
  return False
  
def addMessage(roomID:int, author:int, content:str):
  addMessageToDB(roomID, author, content, datetime.utcnow())

def createNewRoom(userID:int, isPrivate:bool, roomName:str)-> int:
  if isPrivate is None:
    isPrivate = False
  roomID = createRoomToDB(userID, isPrivate, roomName)
  return roomID

def getUsersRooms(userID: int):
  rooms = getUsersRoomsfromDB(userID)
  roomList = []
  for room in rooms:
    roomList.append(
      Room(room[0], room[1], room[3], room[2])
    )
  return roomList

def getRoomTitle(roomID: int, userID: int):
  if checkUserAccessToRoom(roomID, userID):
    return None
  return getRoomTitleFromDB(roomID)

def getIsRoomPrivate(roomID: int):
  roomDetails = getIsRoomInfo(roomID)
  if type(roomDetails[3]) is bool:
    return roomDetails[3]
  return True

def getUsersInRoom(roomID: int, getNonMembers: bool = False):  
  if getNonMembers:
    users = getUsersNotInRoomFromDB(roomID)
  else:
    users = getUsersInRoomFromDB(roomID)
  userList = []
  for user in users:
    userList.append(
      SimpleUser(user[1], user[0])
    )
  return userList

def addUserToPrivateRoom(userID: int, roomID: int):
  addUserToRoomInDB(userID, roomID)

def getRoomAdmin(roomID: int):
  roomInfo = getIsRoomInfo(roomID)
  if not roomInfo == None:
    return roomInfo[2]
  else:
    return -1

def removeUserFromRoom(userID: int, roomID: int):
  removeUserFromRoomInDB(userID, roomID)

