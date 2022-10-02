from enum import Enum
import uuid

class Roles(Enum):
  ADMIN = 0
  USER = 1

class User:
  def __init__(self, username, password, role = Roles.ADMIN):
    self.username = username
    self.password = password
    self.uuid = str(uuid.uuid1())
    self.role = role

class SimpleUser:
    def __init__(self, username, id):
      self.username = username
      self.id = id

class Message:
  def __init__(self, id:int, author:str, room:int, content:str, likes:int, postedTime:str, roomName:str, privateRoom:bool):
    self.id = id
    self.author = author
    self.room = room
    self.content = content
    self.likes = likes
    self.postedTime = postedTime
    self.roomName = roomName
    self.privateRoom = privateRoom
    
class Room:
  def __init__(self, id:int, title:str, creator:str = "public", isPrivate:bool = False):
    self.id = id
    self.title = title
    self.creator = creator
    self.isPrivate = isPrivate
  

    