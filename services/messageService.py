from datetime import datetime
from models import Message, Room
from db import addMessageToDB, createRoomToDB, getMessagesInRoomFromDB, getUsersRoomsfromDB


def getMessagesInRoom(roomID: int=1):
  messagesResult = getMessagesInRoomFromDB(roomID)
  messageArray =  []
  
  for msg in messagesResult:
    messageArray.append(Message(msg[0], msg[6], roomID, msg[3], msg[4], msg[5]))
  
  return list(reversed(messageArray))
  
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