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
    