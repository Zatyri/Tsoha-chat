from db import addUserToDatabase, checkIfUserExcistsinDatabase, getUsersPasswordAndID
from models import User
from werkzeug.security import check_password_hash

def checkIfUserExists(user: str) -> bool:
  return checkIfUserExcistsinDatabase(user)
  
def addUser(user: User) -> bool:
  return addUserToDatabase(user)

def userLogin(username: str, password: str) -> int:
  passwordAndID = getUsersPasswordAndID(username)
  if check_password_hash(passwordAndID[1], password):
    return passwordAndID[0]
  return -1
